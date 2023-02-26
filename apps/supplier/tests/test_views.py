from django.test import RequestFactory, TestCase
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.urls import reverse
import random
import string

from apps.supplier.models import Supplier
from apps.supplier.views import SupplierListView
from .factories import SupplierFactory


class SupplierListViewTestCase(TestCase):
    def setUp(self):
        # create some test data
        self.user = User.objects.create_user(
            username='testuser', password='secret'
        )
        self.factory = RequestFactory()
        self.suppliers = []
        for i in range(15):
            tin = str(random.randint(100000000, 999999999))  # Generate random 9-digit string
            supplier = SupplierFactory(
                company=f'Supplier {i}',
                is_active=True,
                TIN_num=tin,
            )
            self.suppliers.append(supplier)

    def test_supplier_list_view(self):
        request = self.factory.get(reverse('supplier:supplier-list'))
        request.user = self.user
        response = SupplierListView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_pagination(self):
        # create a request and pass it to the view
        request = self.factory.get(reverse('supplier:supplier-list'))
        request.user = self.user
        response = SupplierListView.as_view()(request)

        # assert that the response has the correct pagination information
        self.assertEqual(response.context_data['paginator'].count, 15)
        self.assertEqual(response.context_data['paginator'].per_page, 5)
        self.assertEqual(len(response.context_data['suppliers']), 5)

        # create a request for the second page
        request = self.factory.get(reverse('supplier:supplier-list'), {'page': 2})
        request.user = self.user
        response = SupplierListView.as_view()(request)

        # assert that the response has the correct pagination information
        self.assertEqual(len(response.context_data['suppliers']), 5)

    def test_active_filter(self):
        # create a request with the active filter set to false
        request = self.factory.get(reverse('supplier:supplier-list'), {'active': 'false'})
        request.user = self.user
        response = SupplierListView.as_view()(request)

        # assert that the response only contains inactive suppliers
        self.assertEqual(response.context_data['paginator'].count, 0)
        self.assertEqual(len(response.context_data['suppliers']), 0)
