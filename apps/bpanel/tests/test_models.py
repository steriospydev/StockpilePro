from django.test import TestCase

from django.contrib.auth.models import User
from apps.bpanel.models import DTask

class DTaskTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.task = DTask.objects.create(
            task='Test task',
            username=self.user,
            completed=False
        )

    def test_task_str(self):
        self.assertEqual(str(self.task), 'Test task')

    def test_task_completed_default(self):
        self.assertFalse(self.task.completed)

    def test_task_timestamp_auto_now_add(self):
        task = DTask.objects.create(
            task='Another task',
            username=self.user,
            completed=False
        )
        self.assertIsNotNone(task.timestamp)

    def test_task_ordering(self):
        task1 = DTask.objects.create(
            task='Task 1',
            username=self.user,
            completed=False
        )
        task2 = DTask.objects.create(
            task='Task 2',
            username=self.user,
            completed=False
        )
        task3 = DTask.objects.create(
            task='Task 3',
            username=self.user,
            completed=False
        )
        tasks = DTask.objects.all()
        self.assertEqual(list(tasks), [task3, task2, task1, self.task])
