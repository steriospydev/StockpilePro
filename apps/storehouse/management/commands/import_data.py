import pandas as pd
from django.core.management.base import BaseCommand
from apps.storehouse.models import Storage, Section, Spot, Bin

class Command(BaseCommand):
    help = 'Import data from Excel file'

    def add_arguments(self, parser):
        parser.add_argument('filename', type=str, help='Excel filename')

    def handle(self, *args, **options):
        filename = options['filename']

        df = pd.read_excel(filename, dtype={'spot_name': str})

        for index, row in df.iterrows():
            storage = Storage.objects.get(storage_name=row['storage'])
            section = Section.objects.get(section_name=row['section'])
            item = f"0{row['spot']}"
            spot = Spot.objects.get(spot_name=item)
            Bin.objects.create(
                storage=storage,
                section=section,
                spot=spot,
                in_use=row['in_use']

            )
            # Storage.objects.create(
            #     storage_name=row['name'],
            # )
            # Section.objects.create(
            #     section_name=row['name'],
            # )
            # item = f"0{row['spot_name']}"
            # Spot.objects.create(spot_name=item)

        self.stdout.write(self.style.SUCCESS('Data imported successfully.'))
