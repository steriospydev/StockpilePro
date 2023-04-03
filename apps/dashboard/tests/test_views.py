from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

from ..models import Todo
from ..invoice.models import Invoice, InvoiceItem
from ..product.models import Product
from ..supplier.models import Supplier
from ..storehouse.models import Storage, Stock


class DashboardViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        self.url = reverse('dashboard:index')

    def test_dashboard_view_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/index.html')
        self.assertContains(response, 'Welcome to your Dashboard')

    def test_dashboard_view_post(self):
        data = {'title': 'Test Todo'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.url)
        todo = Todo.objects.first()
        self.assertEqual(todo.title, 'Test Todo')


class TodoRemoveViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        self.todo = Todo.objects.create(title='Test Todo', username=self.user)
        self.url = reverse('dashboard:remove', args=[self.todo.id])

    def test_todo_remove_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('dashboard:index'))
        todos = Todo.objects.filter(username=self.user)
        self.assertEqual(len(todos), 0)


class TodoChangeStatusViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        self.todo = Todo.objects.create(title='Test Todo', username=self.user)
        self.url = reverse('dashboard:change_status', args=[self.todo.id])

    def test_todo_change_status_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('dashboard:index'))
        todo = Todo.objects.get(id=self.todo.id)
        self.assertEqual(todo.completed, True)


class OpsReportViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('dashboard:ops_report')

    def test_ops_report_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/report.html')
        self.assertContains(response, 'Operations Report')
