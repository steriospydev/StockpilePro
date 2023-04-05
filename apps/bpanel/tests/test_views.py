from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission

from apps.bpanel.models import DTask
from apps.bpanel.forms import DTaskForm

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

    def test_ops_report_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('bpanel:report'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bpanel/report.html')
        self.assertIn('product_sold', response.context)
        self.assertIn('supplier_info', response.context)
        self.assertIn('product_in_storages', response.context)
        self.assertIn('most_retrieved_product', response.context)
