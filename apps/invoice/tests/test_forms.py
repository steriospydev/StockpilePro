import pytz
import datetime

from django.test import TestCase
from apps.invoice.models import Invoice, InvoiceItem
from apps.supplier.models import Supplier
from apps.invoice.forms import InvoiceItemForm
from apps.product.models import (Product, Category, SubCategory,
                                 Material, Package, Tax)


timezone = pytz.timezone('Europe/Athens')
now = datetime.datetime.now()

# make the datetime object aware by attaching the timezone object
now_aware = timezone.localize(now)
class InvoiceItemFormTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(category_name='Test Category')

        self.subcategory = SubCategory.objects.create(
            subcategory_name='Test Sub 1', category=self.category)
        self.material = Material.objects.create(material_name='Test material')
        self.package = Package.objects.create(material=self.material, package_quantity=330)
        self.tax_1 = Tax.objects.create(value=13)
        self.supplier = Supplier.objects.create(
            company="Test3 supplier",
            TIN_num="123460890"
        )
        self.product = Product.objects.create(product_name='Test Product',
                                              subcategory=self.subcategory,
                                              package=self.package,
                                              tax_rate=self.tax_1
                                              )
        self.invoice = Invoice(invoice_no=321,
                               supplier=self.supplier,
                               date_of_issuance=now_aware)
        self.invoice.save()

    def test_valid_form(self):
        data = {
            'product': self.product.id,
            'quantity': 2,
            'unit_price': 10.00,
            'invoice': self.invoice.id,
        }
        form = InvoiceItemForm(data=data)
        self.assertTrue(form.is_valid())

    def test_blank_data(self):
        form = InvoiceItemForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 3)

    def test_invalid_quantity(self):
        data = {
            'product': self.product.id,
            'quantity': -2,
            'unit_price': 10.00,
            'invoice': self.invoice.id,
        }
        form = InvoiceItemForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)
        self.assertTrue('quantity' in form.errors)

    def test_invalid_unit_price(self):
        data = {
            'product': self.product.id,
            'quantity': 2,
            'unit_price': -10.00,
            'invoice': self.invoice.id,
        }
        form = InvoiceItemForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)
        self.assertTrue('unit_price' in form.errors)

    def test_product_queryset(self):
        form = InvoiceItemForm()
        self.assertTrue(isinstance(form.fields['product'].queryset.first(), Product))
