from django.core.validators import RegexValidator
from django.db import models
from django.db.models.signals import pre_save
from django.urls import reverse

from apps.utils import abmodels, utils


class Supplier(abmodels.AbstractModel):
    company = models.CharField("Επιχειρηση", max_length=120, unique=True)
    sku_num = models.CharField(max_length=2, unique=True,
                               blank=True, null=True, editable=False)

    class Meta:
        verbose_name = 'Supplier'
        verbose_name_plural = 'Suppliers'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.company}'

    def get_absolute_url(self):
        return reverse('supplier:supplier-detail', args=[str(self.id)])

class Contact(abmodels.AbstractModel):
    supplier = models.OneToOneField(Supplier, on_delete=models.CASCADE)
    person = models.CharField("Eκπροσωπος", max_length=120, blank=True)
    phone = models.CharField(
        'Τηλεφωνο',
        max_length=10,
        blank=True,
        validators=[
            RegexValidator(
                regex=r'^\d{10}$',
                message="Phone number must be entered as 10 digits.No other punctuation required."
            )])
    email = models.CharField(
        'Email',
        max_length=200,
        blank=True,
        validators=[
            RegexValidator(
                regex=r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+',
                message="Wrong email Format."
            )])

    class Meta:
        verbose_name = 'Contact'
        verbose_name_plural = 'Contacts'

    def __str__(self):
        return f'{self.person}'

class Address(abmodels.AbstractModel):
    supplier = models.OneToOneField(Supplier, on_delete=models.CASCADE)
    city = models.CharField('Πολη', max_length=200, blank=True)
    area = models.CharField('Περιοχη', max_length=200, blank=True)
    address = models.CharField('Διευθυνση', max_length=200)
    zipcode = models.CharField(
        'Τ.Κ.',
        max_length=5,
        blank=True,
        validators=[
            RegexValidator(
                regex=r'^\d{5}$',
                message="Zipcode must be 5 digits."
            )])

    class Meta:
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'

    def __str__(self):
        return f'{self.address}'

class TIN(abmodels.AbstractModel):
    supplier = models.OneToOneField(Supplier, on_delete=models.CASCADE)
    TIN_agency = models.CharField("ΔΟΥ", max_length=120)
    TIN_num = models.CharField("Α.Φ.Μ",
                               max_length=9,
                               validators=[
                                   RegexValidator(
                                       regex=r"^[0-9]{9}$",
                                       message="Invalid Greek TIN number. It must contain 9 digits."
                                   )],
                               unique=True)

    class Meta:
        verbose_name = 'TIN'
        verbose_name_plural = 'TIN'

    def __str__(self):
        return f'{self.TIN_num}'

# Delete
class Quote(abmodels.AbstractModel):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    quote = models.CharField(max_length=220)
    type = models.CharField(
        max_length=20,
        choices=[
            ('email', 'Email'),
            ('phone', 'Phone'),
            ('text', 'Text'),
        ],
        default='text')

    def __str__(self):
        return f'{self.quote}'


pre_save.connect(lambda sender, instance, **kwargs:
                 utils.generate_sku_num(sender, instance, k=2),
                 sender=Supplier)
