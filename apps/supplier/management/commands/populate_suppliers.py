from faker import Faker
import random

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from apps.supplier.models import Supplier


class Command(BaseCommand):
    help = 'Populate the database with fake Supplier data'

    def handle(self, *args, **options):
        raise NotImplementedError
