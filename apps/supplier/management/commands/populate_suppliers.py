from faker import Faker
import random

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from apps.supplier.models import Supplier, Address, Contact, TIN


class Command(BaseCommand):
    help = 'Populate the database with fake Supplier data'

    def handle(self, *args, **options):
        fake = Faker()

        for i in range(10):
            company = fake.company()
            address = fake.street_address()
            city = fake.city()
            phone = str(random.randint(1000000000, 9999999999))
            tin_num = str(random.randint(1000000000, 9999999999))
            tin_agency = fake.word()

            supplier = Supplier.objects.create(company=company)
            address = Address.objects.create(supplier=supplier, address=address, city=city)
            contact = Contact.objects.create(supplier=supplier, phone=phone)
            tin = TIN.objects.create(supplier=supplier, TIN_num=tin_num, TIN_agency=tin_agency)

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with fake Supplier data'))
