import pytz
import datetime
from decimal import Decimal
from django.test import TestCase
from django.urls import reverse
from django.db import IntegrityError

from apps.invoice.models import Invoice, InvoiceItem
from apps.supplier.models import Supplier
from apps.product.models import (Product, Category, SubCategory,
                                 Material, Package, Tax)

timezone = pytz.timezone('Europe/Athens')
now = datetime.datetime.now()

# make the datetime object aware by attaching the timezone object
now_aware = timezone.localize(now)

class TestInvoiceModels(TestCase):

    def setUp(self):
        # Create category
        self.category = Category.objects.create(category_name='Test Category')

        # Create subcategory
        self.subcategory = SubCategory.objects.create(
            subcategory_name='Test Sub 1', category=self.category)

        # Create material
        self.material = Material.objects.create(material_name='Test material')

        # Create package
        self.package = Package.objects.create(material=self.material, package_quantity=330)

        # Create taxes
        self.tax_1 = Tax.objects.create(value=13)
        self.tax_2 = Tax.objects.create(value=24)

        # Create products
        self.product_1 = Product.objects.create(
            product_name='Product 1',
            subcategory=self.subcategory,
            package=self.package,
            tax_rate=self.tax_1
        )

        self.product_2 = Product.objects.create(
            product_name='Product 2',
            subcategory=self.subcategory,
            package=self.package,
            tax_rate=self.tax_2
        )

        # Create supplier
        self.supplier = Supplier.objects.create(
            company="Test3 supplier",
            TIN_num="123460890"
        )

        # Create invoice
        self.invoice = Invoice(
            invoice_no=321,
            supplier=self.supplier,
            date_of_issuance=now_aware
        )
        self.invoice.save()

        # Create invoice items
        self.invoice_item_1 = InvoiceItem.objects.create(
            invoice=self.invoice,
            product=self.product_1,
            quantity=5,
            tax_rate=self.tax_1,
            unit_price=1
        )

        self.invoice_item_2 = InvoiceItem.objects.create(
            invoice=self.invoice,
            product=self.product_2,
            quantity=50,
            tax_rate=self.tax_2,
            unit_price=5
        )

    def test_calculate_subtotal(self):
        expected_subtotal = (self.invoice_item_1.quantity * self.invoice_item_1.unit_price) + \
                        (self.invoice_item_2.quantity * self.invoice_item_2.unit_price)
        self.assertEqual(self.invoice.calculate_subtotal(), expected_subtotal)

    def test_get_tax_total(self):
        expected_tax_total_1 = (self.invoice_item_1.quantity * (self.invoice_item_1.tax_rate / Decimal(100)) *
                                self.invoice_item_1.unit_price).quantize(Decimal('0.00'))

        expected_tax_total_2 = (self.invoice_item_2.quantity * (self.invoice_item_2.tax_rate / Decimal(100)) *
                                self.invoice_item_2.unit_price).quantize(Decimal('0.00'))

        self.assertEqual(self.invoice_item_1.get_tax_total, expected_tax_total_1)
        self.assertEqual(self.invoice_item_2.get_tax_total, expected_tax_total_2)

    def test_get_line_subtotal(self):
        expected_line_subtotal_1 = self.invoice_item_1.quantity * self.invoice_item_1.unit_price
        expected_line_subtotal_2 = self.invoice_item_2.quantity * self.invoice_item_2.unit_price

        self.assertEqual(self.invoice_item_1.get_line_subtotal(), expected_line_subtotal_1)
        self.assertEqual(self.invoice_item_2.get_line_subtotal(), expected_line_subtotal_2)

    def test_unique_invoice_item(self):
        # try adding an invoice item with the same product in the same invoice
        with self.assertRaises(IntegrityError):
            InvoiceItem.objects.create(
                invoice=self.invoice,
                product=self.product_1,
                quantity=10,
                tax_rate=self.tax_1,
                unit_price=2
            )

    def test_unique_invoice(self):
        # try adding an invoice item with the same product in the same invoice
        with self.assertRaises(IntegrityError):
            Invoice.objects.create(
                invoice_no=321,
                supplier=self.supplier,
                date_of_issuance=now_aware
            )

    def test_calculate_total_taxes(self):
        expected_total_taxes = self.invoice_item_1.get_tax_total + self.invoice_item_2.get_tax_total
        self.assertEqual(self.invoice.calculate_total_taxes(), expected_total_taxes)

    def test_get_invoice_items(self):
        invoice_items = self.invoice.invoice_items.all()
        self.assertEqual(len(invoice_items), 2)
        self.assertEqual(invoice_items[0].product, self.product_1)
        self.assertEqual(invoice_items[1].product, self.product_2)

    def test_invoice_str_method(self):
        expected_output = f'{self.supplier.company} - {self.invoice.invoice_no}'
        self.assertEqual(str(self.invoice), expected_output)
