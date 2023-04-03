from django.test import TestCase
from django.contrib.auth.models import User
from apps.dashboard.models import Todo

class TodoModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpass')
        self.todo = Todo.objects.create(
            task='Test Task',
            completed=False,
            username=self.user
        )

    def test_todo_str(self):
        self.assertEqual(str(self.todo), 'Test Task')

    def test_todo_ordering(self):
        Todo.objects.create(
            task='New Task',
            completed=False,
            username=self.user
        )
        todos = Todo.objects.all()
        self.assertEqual(todos[0].task, 'New Task')
        self.assertEqual(todos[1], self.todo)
        self.assertEqual(len(todos), 2)

    def test_todo_completed_default(self):
        self.assertFalse(self.todo.completed)

    def test_todo_username_foreign_key(self):
        self.assertEqual(self.todo.username, self.user)
