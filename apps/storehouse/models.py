from django.db import models
from django.urls import reverse
# Create your models here.
from apps.utils import abmodels

# storage_name=A-Z, unique
class Storage(abmodels.AbstractModel):
    storage_name = models.CharField("Ονομασία", unique=True, max_length=1)
    capacity = models.CharField("Χωρητικότητα", max_length=120, blank=True, null=True)
    location = models.CharField("Τοποθεσια", max_length=120, blank=True, null=True)
    summary = models.TextField("Περιγραφή", blank=True, null=True)

    class Meta:
        verbose_name = 'Αποθηκη'
        verbose_name_plural = 'Αποθηκες'

    def __str__(self):
        return f'{self.name}'

# section_name = A-Z, unique
class Section(abmodels.AbstractModel):
    section_name = models.CharField('Μπλόκ', max_length=1, unique=True)

    class Meta:
        verbose_name = 'Μπλοκ'
        verbose_name_plural = 'Μπλοκς'

    def __str__(self):
        return f'{self.section_name}'

class Spot(abmodels.AbstractModel):
    spot_name = models.CharField('Μπλόκ', max_length=1, unique=True)


