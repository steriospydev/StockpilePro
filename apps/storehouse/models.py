from django.db import models
from django.urls import reverse
from django.core.validators import RegexValidator
# Create your models here.
from apps.utils import abmodels

class Storage(abmodels.TimeStamp):
    storage_name = models.CharField("Ονομασία",
                                    unique=True,
                                    max_length=1,
                                    validators=[RegexValidator(
                                        regex=r'^[A-Z]$',
                                        message='The storage name must be a'
                                                ' single uppercase letter from'
                                                ' A to Z',
                                        code='invalid_storage_name')])
    capacity = models.CharField("Χωρητικότητα", max_length=120, blank=True, null=True)
    location = models.CharField("Τοποθεσια", max_length=120, blank=True, null=True)
    summary = models.TextField("Περιγραφή", blank=True, null=True)

    class Meta:
        verbose_name = 'Αποθηκη'
        verbose_name_plural = 'Αποθηκες'

    def __str__(self):
        return f'{self.storage_name}'

class Section(abmodels.TimeStamp):
    section_name = models.CharField('Μπλόκ', unique=True,
                                    max_length=1,
                                    validators=[RegexValidator(
                                        regex=r'^[A-Z]$',
                                        message='The section name'
                                                ' must be a single uppercase'
                                                ' letter from A to Z',
                                        code='invalid_storage_name')])

    class Meta:
        verbose_name = 'Διαδρομος'
        verbose_name_plural = 'Διαδρομοι'

    def __str__(self):
        return f'{self.section_name}'

class Spot(abmodels.TimeStamp):
    spot_name = models.CharField('Θεση', unique=True,
                                 max_length=3,
                                 default='000',
                                 validators=[RegexValidator(
                                    regex=r'^[0-9]{3}$',
                                    message='Η τιμή πρέπει να είναι από '
                                            '001 έως 999',)]
                                 )

    class Meta:
        verbose_name = 'Θεση'
        verbose_name_plural = 'Θεσεις'

    def __str__(self):
        return f'{self.spot_name}'

class BinType(models.Model):
    SHELF = 'S'
    FLOOR = 'F'
    BIN_TYPE_CHOICES = [
        (SHELF, 'Shelf'),
        (FLOOR, 'Floor'),
    ]
    bin_type = models.CharField(
        max_length=1,
        choices=BIN_TYPE_CHOICES,
        default=FLOOR,
    )

    class Meta:
        abstract = True

class UseManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(in_use=True)


class Bin(abmodels.TimeStamp, BinType):
    storage = models.ForeignKey(Storage, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    spot = models.ForeignKey(Spot, on_delete=models.CASCADE)
    in_use = models.BooleanField('Σε χρηση', default=False)

    objects = models.Manager()
    occupied = UseManager()

    class Meta:
        verbose_name = 'Θεση αποθηκευσης'
        verbose_name_plural = 'Θεσεις αποθηκευσης'
        constraints = [
            models.UniqueConstraint(fields=['storage', 'section', 'spot', 'bin_type'],
                                    name='unique_bin')]
        ordering = ['storage', 'section', 'bin_type', 'spot']

    def __str__(self):
        return f'{self.section}-{self.spot}{self.bin_type}'
