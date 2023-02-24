import pandas as pd
from django.core.management.base import BaseCommand
from apps.product.models import Material, Category, SubCategory, Brand

class Command(BaseCommand):
    help = 'Import data from Excel file'

    def add_arguments(self, parser):
        parser.add_argument('filename', type=str, help='Excel filename')

    def handle(self, *args, **options):
        filename = options['filename']
        # dtype={'spot_name': str}
        df = pd.read_excel(filename)

        for index, row in df.iterrows():
            if not pd.isnull(row['material_name']):
                Material.objects.create(material_name=row['material_name'])
            if not pd.isnull(row['category_name']):
                Category.objects.create(category_name=row['category_name'])
            if not pd.isnull(row['brand_name']):
                Brand.objects.create(brand_name=row['brand_name'])

        self.stdout.write(self.style.SUCCESS('Data imported successfully.'))
