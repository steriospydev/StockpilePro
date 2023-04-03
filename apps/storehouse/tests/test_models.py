from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError

from apps.storehouse.models import Storage, Section, Spot, Bin

class StorageModelTest(TestCase):

    def test_storage_name_max_length(self):
        """
        Test that storage_name has a max length of 1 character
        """
        storage = Storage(storage_name='AB')
        with self.assertRaises(ValidationError):
            storage.full_clean()

    def test_storage_name_valid_characters(self):
        """
        Test that storage_name can only contain uppercase letters
        """
        storage = Storage(storage_name='a')
        with self.assertRaises(ValidationError):
            storage.full_clean()

    def test_storage_str_method(self):
        """
        Test that the __str__ method returns the storage_name
        """
        storage = Storage(storage_name='A')
        self.assertEqual(str(storage), 'A')

class SectionModelTest(TestCase):

    def test_section_name_max_length(self):
        """
        Test that section_name has a max length of 1 character
        """
        section = Section(section_name='AB')
        with self.assertRaises(ValidationError):
            section.full_clean()

    def test_section_name_valid_characters(self):
        """
        Test that section_name can only contain uppercase letters
        """
        section = Section(section_name='a')
        with self.assertRaises(ValidationError):
            section.full_clean()

    def test_section_str_method(self):
        """
        Test that the __str__ method returns the section_name
        """
        section = Section(section_name='A')
        self.assertEqual(str(section), 'A')

class SpotModelTest(TestCase):

    def test_spot_name_valid_characters(self):
        """
        Test that spot_name can only contain 3-digit numbers
        """
        spot = Spot(spot_name='a')
        with self.assertRaises(ValidationError):
            spot.full_clean()

    def test_spot_str_method(self):
        """
        Test that the __str__ method returns the spot_name
        """
        spot = Spot(spot_name='001')
        self.assertEqual(str(spot), '001')

class BinModelTest(TestCase):

    def setUp(self):
        self.storage = Storage.objects.create(storage_name='A', capacity='10', location='NY', summary='Some summary')
        self.section = Section.objects.create(section_name='A')
        self.spot = Spot.objects.create(spot_name='001')
        self.bin_type = Bin.FLOOR
        self.bin = Bin.objects.create(storage=self.storage, section=self.section,
                                      spot=self.spot, )

    def test_bin_str_method(self):
        """
        Test that the __str__ method returns the bin location in the format
        'section-spot-bin_type'
        """
        self.assertEqual(str(self.bin), 'A/A-001F')

    def test_bin_uniqueness(self):
        bin2 = Bin(storage=self.storage, section=self.section, spot=self.spot, bin_type=self.bin_type)
        with self.assertRaises(ValidationError):
            bin2.full_clean()

class ModelUniquenessTest(TestCase):

    def test_storage_unique_key(self):
        # create a storage with storage_name 'A'
        storage_a = Storage.objects.create(storage_name='A', capacity='10', location='NY', summary='Some summary')

        # create a new storage with the same storage_name
        with self.assertRaises(IntegrityError):
            storage_a_duplicate = Storage.objects.create(storage_name='A', capacity='5', location='LA', summary='Another summary')

    def test_section_unique_key(self):
        # create a section with section_name 'A'
        section_a = Section.objects.create(section_name='A')

        # create a new section with the same section_name
        with self.assertRaises(IntegrityError):
            section_a_duplicate = Section.objects.create(section_name='A')

    def test_spot_unique_key(self):
        # create a spot with spot_name '001'
        spot_001 = Spot.objects.create(spot_name='001')

        # create a new spot with the same spot_name
        with self.assertRaises(IntegrityError):
            spot_001_duplicate = Spot.objects.create(spot_name='001')

class StorageModelManagerTest(TestCase):
    def setUp(self):
        self.storage = Storage.objects.create(storage_name='A')

        # Create bins for this storage
        self.bin1 = Bin.objects.create(
            storage=self.storage,
            section=Section.objects.create(section_name='A'),
            spot=Spot.objects.create(spot_name='001'),
            bin_type=Bin.FLOOR
        )
        self.bin2 = Bin.objects.create(
            storage=self.storage,
            section=Section.objects.create(section_name='B'),
            spot=Spot.objects.create(spot_name='002'),
            bin_type=Bin.FLOOR
        )

        # Set in_use flag for bin2 to False
        self.bin2.in_use = False
        self.bin2.save()

    def test_use_manager_filters_in_use_bins(self):
        # Check that the UseManager only returns bins with in_use=True
        self.assertEqual(Bin.objects.count(), 2)
        self.assertEqual(len(Bin.occupied.all()), len(Bin.objects.filter(in_use=True)))
