from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from apps.supplier.models import Supplier
from .factories import SupplierFactory


class SupplierTestCase(TestCase):
    def setUp(self):
        self.supplier = SupplierFactory()

    def test_supplier_instance_creation(self):
        self.assertTrue(self.supplier.company, self.supplier.__str__())
        self.assertIsInstance(self.supplier, Supplier)

    def test_get_absolute_url(self):
        url = self.supplier.get_absolute_url()
        self.assertEqual(url, reverse('supplier:supplier-detail', args=[str(self.supplier.id)]))

    def test_sku_num_unique(self):
        with self.assertRaises(IntegrityError):
            SupplierFactory(sku_num=self.supplier.sku_num)

    def test_sku_num_length(self):
        self.assertTrue(len(self.supplier.sku_num), 2)

    def test_unique_tin(self):
        with self.assertRaises(IntegrityError):
            SupplierFactory(TIN_num=self.supplier.TIN_num)

    def test_tin_length(self):
        self.assertTrue(len(self.supplier.TIN_num), 9)
