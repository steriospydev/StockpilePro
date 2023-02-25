from django.db import models
from django.db.models.signals import pre_save

from apps.utils import abmodels, signals

KILO = 'kg'
GRAMMS = 'gr'
OTHER = 'oo'
LITRES = 'lt'
MILLILITRES = 'ml'
UNIT = 'τx'

PACKAGE_UNITS_CHOICES = [
    (KILO, 'Kilo'),
    (GRAMMS, 'Gramms'),
    (LITRES, 'Litre'),
    (MILLILITRES, 'Millilitre'),
    (UNIT, 'Τεμαχιο'),
]


class CategoryTempValues(models.Model):
    """
     Variables for template rendering,
     each category will have its
     icon:mdi library
     colour:bulma classes.
    """
    primary_colour = models.CharField(max_length=220, null=True,
                                      blank=True,
                                      default='has-background-dark')
    icon = models.CharField(max_length=220, null=True,
                            blank=True,
                            default='mdi mdi-account-multiple')
    icon_size = models.CharField(max_length=220, null=True,
                                 blank=True,
                                 default='mdi-48px')

    class Meta:
        abstract = True

class Category(CategoryTempValues):
    category_name = models.CharField("Ονομα", unique=True, max_length=120)

    class Meta:
        verbose_name = 'Κατηγορια'
        verbose_name_plural = 'Κατηγοριες'
        ordering = ['category_name']

    def __str__(self):
        return f'{self.category_name}'

    def get_num_products(self):
        subcategories = self.subs.all()
        return sum(subcategory.get_num_products() for subcategory in subcategories)

class Material(models.Model):
    material_name = models.CharField("Ονομα", unique=True, max_length=120)

    class Meta:
        verbose_name = 'Υλικο'
        verbose_name_plural = 'Υλικα'

    def __str__(self):
        return f'{self.material_name}'

class SubCategory(models.Model):
    subcategory_name = models.CharField("Ονομασια", max_length=120)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 related_name='subs')

    class Meta:
        verbose_name = 'Υποκατηγορια'
        verbose_name_plural = 'Υποκατηγοριες'
        constraints = [
            models.UniqueConstraint(fields=['subcategory_name', 'category'],
                                    name='unique_category')]

    def __str__(self):
        return f'{self.subcategory_name} - {self.category}'

    def get_num_products(self):
        products = self.sub_products.all()
        return len(products)

class Package(models.Model):
    material = models.ForeignKey(Material, on_delete=models.CASCADE,
                                 related_name='packages')
    package_unit = models.CharField("M.M.", max_length=2,
                                    choices=PACKAGE_UNITS_CHOICES, default=OTHER)
    package_quantity = models.BigIntegerField("Ποσοτητα", default=0)

    class Meta:
        verbose_name = 'Συσκευασια'
        verbose_name_plural = 'Συσκευασιες'
        constraints = [
            models.UniqueConstraint(fields=['material', 'package_unit',
                                            'package_quantity'],
                                    name='unique_package')
        ]

    def __str__(self):
        return f'{self.package_quantity}{self.package_unit} {self.material}'

class Product(abmodels.TimeStamp):
    product_name = models.CharField("Ονομασια", max_length=120)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE,
                                    related_name='sub_products')
    package = models.ForeignKey(Package, on_delete=models.CASCADE,
                                related_name='package_products')
    summary = models.TextField("Περιγραφη", null=True, blank=True)
    sku_num = models.CharField(max_length=3, unique=True,
                               blank=True, null=True, editable=False)
    image = models.ImageField("Φωτογραφια", upload_to='product_images', null=True, blank=True)

    class Meta:
        verbose_name = 'Προιον'
        verbose_name_plural = 'Προιοντα'
        constraints = [
            models.UniqueConstraint(fields=['product_name', 'package'],
                                    name='unique_product')
        ]

    def __str__(self):
        return f'{self.product_name} - {self.package}'


pre_save.connect(lambda sender, instance, **kwargs:
                 signals.generate_sku_num(sender, instance, k=3),
                 sender=Product)
