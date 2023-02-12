from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.test import TestCase

from apps.supplier.models import Supplier, TIN, Contact, Address, Quote
from .factories import (SupplierFactory, TINFactory,
                        ContactFactory, AddressFactory, QuoteFactory)


class SupplierTestCase(TestCase):
    def test_supplier_instance_creation(self):
        supplier = SupplierFactory()
        self.assertIsInstance(supplier, Supplier)

    def test_sku_num_unique(self):
        supplier1 = SupplierFactory()
        with self.assertRaises(IntegrityError):
            SupplierFactory(sku_num=supplier1.sku_num)

class TinTestCase(TestCase):
    def test_tin_creation(self):
        tin = TINFactory()
        self.assertTrue(isinstance(tin, TIN))
        self.assertEqual(str(tin), tin.TIN_num)
        self.assertTrue(isinstance(tin.supplier, Supplier))

    def test_tin_supplier_relation(self):
        tin = TINFactory()
        supplier1 = tin.supplier
        self.assertTrue(tin.supplier, supplier1)
        self.assertEqual(tin.supplier_id, supplier1.id)
        with self.assertRaises(IntegrityError):
            TINFactory(supplier=supplier1)

class AddressTestCase(TestCase):
    def test_address_creation(self):
        address = AddressFactory()
        self.assertEqual(str(address), address.address)
        self.assertTrue(isinstance(address, Address))
        self.assertTrue(isinstance(address.supplier, Supplier))

    def test_address_supplier_relation(self):
        address = AddressFactory()
        supplier1 = address.supplier
        self.assertTrue(address.supplier, supplier1)
        self.assertEqual(address.supplier_id, supplier1.id)
        with self.assertRaises(IntegrityError):
            AddressFactory(supplier=supplier1)

class ContactTestCase(TestCase):
    def test_contact_creation(self):
        contact = ContactFactory()
        self.assertEqual(str(contact), contact.person)
        self.assertTrue(isinstance(contact, Contact))
        self.assertTrue(isinstance(contact.supplier, Supplier))

    def test_address_supplier_relation(self):
        contact = ContactFactory()
        supplier1 = contact.supplier
        self.assertTrue(contact.supplier, supplier1)
        self.assertEqual(contact.supplier_id, supplier1.id)
        with self.assertRaises(IntegrityError):
            ContactFactory(supplier=supplier1)

class QuoteTestCase(TestCase):
    def test_create_quote(self):
        quote = QuoteFactory()
        self.assertIsInstance(quote, Quote)
        self.assertIsInstance(quote.supplier, Supplier)
        self.assertIsNotNone(quote.pk)
        self.assertIsNotNone(quote.created_at)
        self.assertIsNotNone(quote.updated_at)

    def test_many_to_one_relationship(self):
        supplier = SupplierFactory()
        quotes = QuoteFactory.create_batch(3, supplier=supplier)
        self.assertEqual(quotes[0].supplier, supplier)
        self.assertEqual(quotes[1].supplier, supplier)
        self.assertEqual(quotes[2].supplier, supplier)

    def test_quote_type_validation(self):
        with self.assertRaises(ValidationError):
            QuoteFactory(type='invalid_quote_type').full_clean()

    def test_summary_validation(self):
        with self.assertRaises(ValidationError):
            QuoteFactory(quote='a' * 221).full_clean()

    def test_summary_char_set(self):
        quote = QuoteFactory(quote='This is a test with special characters: 🚀')
        self.assertEqual(quote.quote, 'This is a test with special characters: 🚀')
