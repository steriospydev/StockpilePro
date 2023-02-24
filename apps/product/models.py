from django.db import models

from apps.utils import abmodels

KILO = 'kg'
GRAMMS = 'gr'
OTHER = 'oo'
LITRES = 'lt'
MILLILITRES = 'ml'
UNIT = 'un'

PACKAGE_UNITS_CHOICES = [
    (KILO, 'Kilo'),
    (GRAMMS, 'Gramms'),
    (LITRES, 'Litre'),
    (MILLILITRES, 'Millilitre'),
    (UNIT, 'Unit'),
]


class Category(models.Model):
    category_name = models.CharField("Ονομα", unique=True, max_length=120)

    class Meta:
        verbose_name = 'Κατηγορια'
        verbose_name_plural = 'Κατηγοριες'

    def __str__(self):
        return f'{self.category_name}'

class Material(models.Model):
    material_name = models.CharField("Ονομα", unique=True, max_length=120)

    class Meta:
        verbose_name = 'Υλικο'
        verbose_name_plural = 'Υλικα'

    def __str__(self):
        return f'{self.material_name}'

class Brand(models.Model):
    brand_name = models.CharField("Ονομα", unique=True, max_length=120)

    def __str__(self):
        return f'{self.brand_name}'

class SubCategory(models.Model):
    subcategory_name = models.CharField("Ονομασια", max_length=120)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 related_name='subs')

    class Meta:
        verbose_name = 'Υποκατηγορια'
        verbose_name_plural = 'Υποκατηγοριες'
        constraints = [
            models.UniqueConstraint(fields=['subcategory_name', 'category'],
                                    name='unique_category')
        ]

    def __str__(self):
        return f'{self.subcategory_name}'

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

class Product(models.Model):
    pass
