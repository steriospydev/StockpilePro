from django.test import TestCase, Client
from django.urls import reverse
from apps.storehouse.models import Storage, Section, Spot, Bin
from .factories import StorageFactory, SectionFactory, SpotFactory, BinFactory


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.storage = StorageFactory()
        self.section = SectionFactory()
        self.spot = SpotFactory()
        self.bin = BinFactory(storage=self.storage, section=self.section, spot=self.spot)

    def test_storehouse_home(self):
        url = reverse('storehouse:storehouse-main')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'storehouse/storehouse_main.html')
        self.assertContains(response, self.storage.storage_name)
        self.assertContains(response, self.bin.bin_type)

    def test_storage_bins_page(self):
        url = reverse('storehouse:storage-detail', args=[self.storage.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'storehouse/storehouse_detail.html')
        self.assertContains(response, self.storage.storage_name)
        self.assertContains(response, self.bin.bin_type)
