# Generated by Django 4.1.6 on 2023-02-08 09:55

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('supplier', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TIN',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Δημιουργηθηκε')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Ανανεωθηκε')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active')),
                ('TIN_agency', models.CharField(max_length=120)),
                ('TIN_num', models.CharField(max_length=9, unique=True, validators=[django.core.validators.RegexValidator(message='Invalid Greek TIN number. It must contain 9 digits.', regex='^[0-9]{9}$')], verbose_name='VAT number')),
                ('supplier', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='supplier.supplier')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.DeleteModel(
            name='VAT',
        ),
    ]
