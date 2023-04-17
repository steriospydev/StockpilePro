from io import BytesIO
import base64
from datetime import datetime
from decimal import Decimal


import unittest.mock as mock
from unittest.mock import patch, Mock
from django.test import TestCase, Client

from django import forms
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission

import matplotlib.pyplot as plt

from apps.bpanel.models import DTask
from apps.bpanel.forms import DTaskForm, ProductChartForm
from apps.bpanel.graphs.product_reports import construct_product_chart
from apps.product.models import Product, Package, Material
from apps.storehouse.models import Stock
from apps.invoice.models import Invoice, InvoiceItem

class TestBPanelViews(TestCase):

    def setUp(self):
        self.client = Client()
        User = get_user_model()
        self.user = User.objects.create_user(
            username='testuser', password='testpass')
        self.index_url = reverse('bpanel:index')
        self.report_url = reverse('bpanel:product-report')

    def test_index_view_with_no_dtask(self):
        self.client.force_login(self.user)
        response = self.client.get(self.index_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bpanel/index.html')

    def test_index_view_with_dtask(self):
        self.client.force_login(self.user)
        DTask.objects.create(task='test task', username=self.user)
        response = self.client.get(self.index_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'test task')

    def test_index_view_post_form_creates_new_dtask(self):
        self.client.force_login(self.user)
        num_dtasks_before = DTask.objects.count()
        response = self.client.post(self.index_url, data={

            'task': 'This is a test task.'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(DTask.objects.count(), num_dtasks_before + 1)
        new_dtask = DTask.objects.latest('id')
        self.assertEqual(new_dtask.task, 'This is a test task.')
        self.assertEqual(new_dtask.username, self.user)

    def test_remove_view_deletes_dtask(self):
        self.client.force_login(self.user)
        task = DTask.objects.create(task='test task', username=self.user)
        remove_url = reverse('bpanel:todo-remove', args=[task.id])
        response = self.client.post(remove_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(DTask.objects.count(), 0)

    def test_change_status_view_changes_task_status(self):
        self.client.force_login(self.user)
        task = DTask.objects.create(task='test task', username=self.user)
        change_status_url = reverse('bpanel:todo-change', args=[task.id])
        response = self.client.post(change_status_url)
        self.assertEqual(response.status_code, 302)
        updated_task = DTask.objects.get(id=task.id)
        self.assertTrue(updated_task.completed)

    def test_change_status_view_changes_task_status_to_false(self):
        self.client.force_login(self.user)
        task = DTask.objects.create(task='test task', username=self.user, completed=True)
        change_status_url = reverse('bpanel:todo-change', args=[task.id])
        response = self.client.post(change_status_url)
        self.assertEqual(response.status_code, 302)
        updated_task = DTask.objects.get(id=task.id)
        self.assertFalse(updated_task.completed)

    def test_ops_report_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('bpanel:report'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bpanel/report.html')
        self.assertIn('product_sold', response.context)
        self.assertIn('supplier_info', response.context)
        self.assertIn('product_in_storages', response.context)
        self.assertIn('most_retrieved_product', response.context)

    def test_ops_report_anonymous(self):
        response = self.client.get(reverse('bpanel:report'))
        # assert response status code
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/?next=/bpanel/report/')

    def test_invoice_chart_view(self):
        self.client.force_login(self.user)
        # Create a dictionary with hardcoded invoice data
        invoice_data = [
            {'month': datetime(2022, 1, 1), 'total': 100},
            {'month': datetime(2022, 2, 1), 'total': 200},
            {'month': datetime(2022, 3, 1), 'total': 300},
        ]

        # Mock the Invoice.objects.annotate method to return the hardcoded data
        with patch('apps.bpanel.views.Invoice.objects.annotate') as mock_annotate:
            mock_annotate.return_value.values.return_value.annotate.return_value.order_by.return_value = invoice_data

            # Make a GET request to the view
            response = self.client.get(reverse('bpanel:invoice-chart'))

            # Check that the response was successful
            self.assertEqual(response.status_code, 200)

            # Check that the expected context variables are present
            self.assertIn('charts', response.context)
            self.assertIn('overall_chart', response.context)

            # Check that the charts are constructed correctly
            charts = response.context['charts']
            self.assertEqual(len(charts), 1)
            self.assertIn(2022, charts)
            self.assertIsInstance(charts[2022], str)

            # Check that the overall chart is constructed correctly
            overall_chart = response.context['overall_chart']
            self.assertIsInstance(overall_chart, str)

    def test_invoice_chart_anonymous(self):
        response = self.client.get(reverse('bpanel:invoice-chart'))
        # assert response status code
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/?next=/bpanel/invoice-chart/')

    def test_product_report_view_with_authenticated_user(self):
        self.client.force_login(self.user)
        response = self.client.get(self.report_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bpanel/product_chart.html')
        self.assertIn('stock_aggregate', response.context)

    def test_product_report_view_with_anonymous_user(self):
        response = self.client.get(self.report_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/?next={self.report_url}')

class GraphsTestCase(TestCase):

    @mock.patch('matplotlib.pyplot.savefig')
    def test_construct_product_chart(self, mock_savefig):
        # Create some example data
        product = [
            {'product_name': 'Product 1', 'package_str': 'Package 1',
             'total_bought': 10, 'total_sold': 5, 'total_available': 5},
            {'product_name': 'Product 2', 'package_str': 'Package 2',
             'total_bought': 20, 'total_sold': 10, 'total_available': 10},
        ]

        # Call the function with the example data
        image_base64 = construct_product_chart(product)

        # Check that the function returns a string
        self.assertIsInstance(image_base64, str)

        # Check that the mock savefig method was called with the expected arguments
        mock_savefig.assert_called_once()
        args, kwargs = mock_savefig.call_args
        self.assertEqual(args[0], mock.ANY)  # Check that the first argument is a file-like object
        self.assertEqual(kwargs['format'], 'png')  # Check that the format is PNG

        # Check that the PNG image can be decoded and is not empty
        image_bytes = args[0].getvalue()
        image_decoded = base64.b64decode(image_base64)
        self.assertEqual(image_bytes, image_decoded)

class ProductChartFormTestCase(TestCase):

    def test_form_choices(self):
        form = ProductChartForm()

        # Assert that product field is a ChoiceField
        self.assertIsInstance(form.fields['product'], forms.ChoiceField)

        # Assert that the choices consist of a list of tuples, where each tuple contains a product id and name
        expected_choices = [(product.id, str(product)) for product in Product.objects.select_related('package__material', 'subcategory')]
        self.assertListEqual(form.fields['product'].choices, expected_choices)
