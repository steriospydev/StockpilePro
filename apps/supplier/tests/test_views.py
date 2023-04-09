import random
import string

from django.test import RequestFactory, TestCase, Client
from django.contrib.auth.models import User, AnonymousUser
from django.core.paginator import Paginator
from django.urls import reverse
from django.http import HttpResponseRedirect


from apps.supplier.models import Supplier
from apps.supplier.views import SupplierListView
from .factories import SupplierFactory


class SupplierListViewTestCase(TestCase):
    def setUp(self):
        # create some test data
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', password='secret'
        )
        self.suppliers = []
        for i in range(15):
            tin = str(random.randint(100000000, 999999999))  # Generate random 9-digit string
            supplier = SupplierFactory(
                company=f'Supplier {i}',
                is_active=True,
                TIN_num=tin,
            )
            self.suppliers.append(supplier)

    def test_template_used(self):
        self.client.login(username='testuser', password='secret')
        response = self.client.get(reverse('supplier:supplier-list'))
        self.assertTemplateUsed(response, 'supplier/supplier_list.html')

    def test_with_authenticated(self):
        self.client.login(username='testuser', password='secret')
        response = self.client.get(reverse('supplier:supplier-list'))
        self.assertEqual(response.status_code, 200)

    def test_with_anonymous(self):
        self.client.logout()
        response = self.client.get(reverse('supplier:supplier-list'))
        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/?next=/supplier/')

    def test_correct_number_of_suppliers(self):
        self.client.login(username='testuser', password='secret')
        response = self.client.get(reverse('supplier:supplier-list'))
        self.assertEqual(len(response.context['suppliers']), len(self.suppliers))

class SupplierCRUDTestCase(TestCase):
    def setUp(self):
        # create some test data
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', password='secret'
        )
        tin = str(random.randint(100000000, 999999999))
        self.supplier = SupplierFactory(
                        company='Supplier Test',
                        is_active=True,
                        TIN_num=tin,
                        sku_num='FF'
                    )

    def test_template_used(self):
        self.client.login(username='testuser', password='secret')
        response = self.client.get(reverse('supplier:supplier-create'))
        self.assertTemplateUsed(response, 'supplier/supplier_create_update.html')

    def test_with_authenticated(self):
        self.client.login(username='testuser', password='secret')
        response = self.client.get(reverse('supplier:supplier-create'))
        self.assertEqual(response.status_code, 200)

    def test_with_anonymous(self):
        self.client.logout()
        response = self.client.get(reverse('supplier:supplier-create'))
        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/?next=/supplier/new/')

    def test_correct_supplier_info(self):
        self.client.login(username='testuser', password='secret')
        data = {
            'company': 'New Supplier',
            'is_active': True,
            'TIN_num': str(random.randint(100000000, 999999999)),
            # add other fields here as necessary
        }
        response = self.client.post(reverse('supplier:supplier-create'), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Supplier.objects.count(), 2)
        new_supplier = Supplier.objects.first()
        self.assertEqual(new_supplier.company, data['company'])
        self.assertEqual(new_supplier.is_active, data['is_active'])
        self.assertEqual(new_supplier.TIN_num, data['TIN_num'])

    def test_template_used_in_detail_view(self):
        self.client.login(username='testuser', password='secret')
        response = self.client.get(reverse('supplier:supplier-detail', args=[self.supplier.id]))
        self.assertTemplateUsed(response, 'supplier/supplier_detail.html')

    def test_delete_view(self):
        self.client.login(username='testuser', password='secret')
        response = self.client.post(reverse('supplier:supplier-delete', args=[self.supplier.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Supplier.objects.count(), 0)
