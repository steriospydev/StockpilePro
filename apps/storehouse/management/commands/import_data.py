import pandas as pd
from django.core.management.base import BaseCommand
from apps.storehouse.models import Storage, Section, Spot

class Command(BaseCommand):
    help = 'Import data from Excel file'

    def add_arguments(self, parser):
        parser.add_argument('filename', type=str, help='Excel filename')

    def handle(self, *args, **options):
        filename = options['filename']

        df = pd.read_excel(filename, dtype={'spot_name': str})

        for index, row in df.iterrows():
            # Storage.objects.create(
            #     storage_name=row['storage_name'],
            # )
            # Section.objects.create(
            #     section_name=row['storage_name'],
            # )
            Spot.objects.create(spot_name=row['spot_name'])

        self.stdout.write(self.style.SUCCESS('Data imported successfully.'))
