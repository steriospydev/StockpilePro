from io import BytesIO
import base64

import unittest.mock as mock
from unittest.mock import patch, Mock
from django.test import TestCase, Client

from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission

import matplotlib.pyplot as plt

from apps.bpanel.models import DTask
from apps.bpanel.forms import DTaskForm
from apps.bpanel.graphs.product_reports import construct_product_chart

class TestBPanelViews(TestCase):

    def setUp(self):
        self.client = Client()
        User = get_user_model()
        self.user = User.objects.create_user(
            username='testuser', password='testpass')
        self.index_url = reverse('bpanel:index')

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

class UtilsTestCase(TestCase):

    @mock.patch('matplotlib.pyplot.savefig')
    def test_construct_product_chart(self, mock_savefig):
        # Create some example data
        product = [
            {'product_name': 'Product 1', 'package_str': 'Package 1', 'total_bought': 10, 'total_sold': 5, 'total_available': 5},
            {'product_name': 'Product 2', 'package_str': 'Package 2', 'total_bought': 20, 'total_sold': 10, 'total_available': 10},
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
