# Generated by Django 4.1.6 on 2023-02-10 01:08

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('supplier', '0002_tin_delete_vat'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='address',
            options={'verbose_name': 'Address', 'verbose_name_plural': 'Addresses'},
        ),
        migrations.AlterModelOptions(
            name='contact',
            options={'verbose_name': 'Contact', 'verbose_name_plural': 'Contacts'},
        ),
        migrations.AlterModelOptions(
            name='supplier',
            options={'ordering': ['-created_at'], 'verbose_name': 'Supplier', 'verbose_name_plural': 'Suppliers'},
        ),
        migrations.AlterModelOptions(
            name='tin',
            options={'verbose_name': 'TIN', 'verbose_name_plural': 'TIN'},
        ),
        migrations.AlterField(
            model_name='tin',
            name='TIN_agency',
            field=models.CharField(max_length=120, verbose_name='ΔΟΥ'),
        ),
        migrations.AlterField(
            model_name='tin',
            name='TIN_num',
            field=models.CharField(max_length=9, unique=True, validators=[django.core.validators.RegexValidator(message='Invalid Greek TIN number. It must contain 9 digits.', regex='^[0-9]{9}$')], verbose_name='Α.Φ.Μ'),
        ),
    ]
