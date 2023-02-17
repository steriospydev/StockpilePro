from django.test import RequestFactory, TestCase
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.urls import reverse

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
        for i in range(15):
            SupplierFactory(company='Supplier {}'.format(i), is_active=True)

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
    #
    # def test_active_filter(self):
    #     # create a request with the active filter set to false
    #     request = self.factory.get(reverse('supplier:supplier-list'), {'active': 'false'})
    #     request.user = self.user
    #     response = SupplierListView.as_view()(request)
    #
    #     # assert that the response only contains inactive suppliers
    #     self.assertEqual(response.context_data['paginator'].count, 0)
    #     self.assertEqual(len(response.context_data['suppliers']), 0)
