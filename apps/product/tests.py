from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError
from django.db.models import Count

from apps.product.models import (Category, SubCategory,
                                 Material, Package,
                                 KILO, GRAMMS, LITRES, MILLILITRES, UNIT,
                                 Tax, Product)
from apps.product.forms import CategoryForm


class CategoryModelTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(category_name='Category 1')

    def test_category_creation(self):
        self.assertTrue(isinstance(self.category, Category))
        self.assertEqual(self.category.__str__(), self.category.category_name)

    def test_category_uniqueness(self):
        with self.assertRaises(Exception):
            Category.objects.create(category_name='Category 1')

    def test_absolute_url_logged_in(self):
        user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('product:category-detail', args=[self.category.id]))
        self.assertEqual(response.status_code, 200)

    def test_absolute_url_no_logged_in(self):
        response = self.client.get(reverse('product:category-detail', args=[self.category.id]))
        self.assertEqual(response.status_code, 302)

class SubCategoryModelTestCase(TestCase):

    def setUp(self):
        self.category = Category.objects.create(category_name="Test Category")
        self.subcategory = SubCategory.objects.create(subcategory_name="Test Subcategory", category=self.category)

    def test_subcategory_creation(self):
        self.assertEqual(self.subcategory.subcategory_name, "Test Subcategory")

    def test_subcategory_uniqueness(self):
        with self.assertRaises(IntegrityError):
            subcategory2 = SubCategory.objects.create(subcategory_name="Test Subcategory", category=self.category)

    def test_absolute_url_logged_in_user(self):
        self.client.force_login(User.objects.create_user(username='testuser', password='12345'))
        response = self.client.get(reverse('product:product-sublist', kwargs={'pk': self.subcategory.pk}))
        self.assertEqual(response.status_code, 200)

    def test_absolute_url_no_user(self):
        response = self.client.get(reverse('product:product-sublist', kwargs={'pk': self.subcategory.pk}))
        self.assertEqual(response.status_code, 302)

    def test_subcategory_different_category_allowed(self):
        category2 = Category.objects.create(category_name="Test Category 2")
        subcategory2 = SubCategory.objects.create(subcategory_name="Test Subcategory", category=category2)
        self.assertEqual(subcategory2.subcategory_name, "Test Subcategory")

class MaterialModelTestCase(TestCase):

    def test_material_creation(self):
        material = Material.objects.create(material_name="Test Material")
        self.assertEqual(material.material_name, "Test Material")

    def test_material_uniqueness(self):
        Material.objects.create(material_name="Test Material")
        with self.assertRaises(IntegrityError):
            Material.objects.create(material_name="Test Material")

class PackageModelTestCase(TestCase):
    def setUp(self):
        self.material = Material.objects.create(material_name="Test Material")
        self.package = Package.objects.create(material=self.material,
                                              package_unit=KILO,
                                              package_quantity=1.5)

    def test_create_package(self):
        self.assertEqual(str(self.package), "1.5kg Test Material")
        self.assertEqual(self.package.material, self.material)
        self.assertEqual(self.package.package_unit, KILO)
        self.assertEqual(self.package.package_quantity, 1.5)

    def test_package_uniqueness(self):
        with self.assertRaises(IntegrityError):
            Package.objects.create(material=self.material,
                                   package_unit=KILO,
                                   package_quantity=1.5)

class TaxModelTestCase(TestCase):
    def test_tax_creation(self):
        # Test creation with valid value
        tax = Tax.objects.create(value=24.0)
        self.assertEqual(str(tax), '24.0')

    def test_tax_creation_with_negative_value(self):
        try:
            Tax.objects.create(value=-5.0)
        except ValidationError as e:
            self.assertEqual(str(e), 'Tax value can not be negative')

    def test_tax_creation_with_invalid_type(self):
        # Test creation with invalid type (string)
        with self.assertRaises(ValidationError):
            Tax.objects.create(value='invalid')

class ProductModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(category_name='test category')
        self.subcategory = SubCategory.objects.create(subcategory_name="test subcategory", category=self.category)
        self.material = Material.objects.create(material_name='test material')
        self.package = Package.objects.create(material=self.material, package_unit=KILO, package_quantity=1)
        self.tax_rate = Tax.objects.create(value=0.24)
        self.product = Product.objects.create(
            product_name="test product",
            subcategory=self.subcategory,
            package=self.package,
            tax_rate=self.tax_rate,
            summary="test summary",
            is_active=True,
            available=True,
            online_sell=True,
        )
        self.user = User.objects.create_user(
            username="testuser", email="testuser@test.com", password="testpass"
        )

    def test_product_creation(self):
        product_count = Product.objects.count()
        self.assertEqual(product_count, 1)

    def test_str_method(self):
        self.assertEqual(str(self.product), "test product - 1kg test material")

    def test_unique_constraint(self):
        # try to create a new product with the same name and package
        new_product = Product(
            product_name="test product", subcategory=self.subcategory, package=self.package
        )
        with self.assertRaises(Exception):
            new_product.save()

    def test_get_absolute_url_logged_in(self):
        self.client.login(username="testuser", password="testpass")
        url = reverse("product:product-detail", args=[str(self.product.id)])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_get_absolute_url_not_logged_in(self):
        url = reverse("product:product-detail", args=[str(self.product.id)])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

class CategoryListViewTestCase(TestCase):
    def setUp(self):
        # Create some categories and products using factories
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpass'
        )
        self.url = reverse('product:category-list')
        self.category = Category.objects.create(category_name='Test category')
        self.subcategory = SubCategory.objects.create(subcategory_name='Test category',
                                                       category=self.category)
        self.material = Material.objects.create(material_name='test material')
        self.package = Package.objects.create(material=self.material,
                                              package_unit=KILO, package_quantity=1)
        self.tax_rate = Tax.objects.create(value=0.24)
        self.product = Product.objects.create(
            product_name="test product",
            subcategory=self.subcategory,
            package=self.package,
            tax_rate=self.tax_rate,
            summary="test summary",
            is_active=True,
            available=True,
            online_sell=True,
        )

    def test_category_list_view(self):
        # log in the user
        self.client.login(username='testuser', password='testpass')

        # get the response and check the status code
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        # check that the template is correct
        self.assertTemplateUsed(response, 'product/category/category_list.html')

        # check that the context contains the expected variables
        self.assertEqual(len(response.context['categories']), 1)
        self.assertEqual(len(response.context['categories'][0].subs.all()), 1)
        self.assertEqual(len(response.context['categories'][0].subs.all()[0].sub_products.all()), 1)
        self.assertEqual(response.context['num_products'], 1)

class CategoryDetailViewTestCase(TestCase):
    def setUp(self):
        # Create a category and some subcategories and products using factories
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpass'
        )
        self.category = Category.objects.create(category_name='Test category')
        self.subcategory1 = SubCategory.objects.create(subcategory_name='Test subcategory 1', category=self.category)
        self.subcategory2 = SubCategory.objects.create(subcategory_name='Test subcategory 2', category=self.category)
        self.material = Material.objects.create(material_name='test material')
        self.package = Package.objects.create(material=self.material,
                                              package_unit=KILO, package_quantity=1)
        self.tax_rate = Tax.objects.create(value=0.24)
        self.product1 = Product.objects.create(
            product_name="Test product 1",
            subcategory=self.subcategory1,
            package=self.package,
            tax_rate=self.tax_rate,
            is_active=True,
            available=True,
            online_sell=True,
        )
        self.product2 = Product.objects.create(
            product_name="Test product 2",
            subcategory=self.subcategory1,
            package=self.package,
            tax_rate=self.tax_rate,
            is_active=True,
            available=True,
            online_sell=True,
        )
        self.product3 = Product.objects.create(
            product_name="Test product 3",
            subcategory=self.subcategory2,
            package=self.package,
            tax_rate=self.tax_rate,
            is_active=True,
            available=True,
            online_sell=True,
        )
        self.url = reverse('product:category-detail', args=[self.category.id])

    def test_category_detail_view_status_code(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_category_detail_view_template_used(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'product/category/category_detail.html')

    def test_category_detail_view_context_data(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(self.url)

        # Assert that the category object in the context is the same as the one in the view
        self.assertEqual(response.context['category'], self.category)

        # Assert that the subcategories in the context are the ones related to the category
        expected_subcategories = self.category.subs.annotate(num_products=Count('sub_products')).order_by(
            'subcategory_name')
        self.assertQuerysetEqual(response.context['subcategories'], expected_subcategories)

        # Assert that the total number of products in the context is correct
        expected_num_products = sum(subcategory.num_products for subcategory in expected_subcategories)
        self.assertEqual(response.context['num_products'], expected_num_products)

class CategoryCreateUpdateTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpass'
        )
        self.client.login(username='testuser', password='testpass')
        self.category = Category.objects.create(category_name='Test category')
        self.url = reverse('product:category-create')
        self.data = {
            'category_name': 'New test category'
        }

    def test_category_create_update_view_uses_correct_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'product/category/category_create_update.html')
