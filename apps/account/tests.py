from django.test import Client, TestCase
from django.contrib.auth.models import User
from django.contrib.auth import views as auth_views
from django.urls import resolve
from django import forms

from apps.account.forms import LoginForm

class BaseTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.username = 'testuser'
        self.email = 'testuser@example.com'
        self.password = 'secret'
        self.user = User.objects.create_user(self.username, self.email, self.password)

class LoginViewTestCase(BaseTestCase):
    def test_login_view_url_resolution(self):
        found = resolve('/')
        self.assertEqual(found.func.__name__, auth_views.LoginView.as_view().__name__)

    def test_login(self):
        response = self.client.post('/', {'username': self.username, 'password': self.password})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/bpanel/', status_code=302)
        self.assertTrue(response.url.endswith('/bpanel/'))
        self.assertTrue(response.wsgi_request.user.is_authenticated)


class IndexViewTestCase(BaseTestCase):
    def test_index_authenticated(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get('/bpanel/')
        self.assertEqual(response.status_code, 200)

    def test_index_unauthenticated(self):
        response = self.client.get('/bpanel/')
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url, '/')

class LoginFormTestCase(TestCase):

    def test_login_form_fields(self):
        form = LoginForm()
        self.assertIsInstance(form.fields['username'], forms.CharField)
        self.assertIsInstance(form.fields['password'], forms.CharField)
        self.assertIsInstance(form.fields['password'].widget, forms.PasswordInput)

    def test_login_form_validation(self):
        form_data = {'username': 'user123', 'password': 'password123'}
        form = LoginForm(data=form_data)
        self.assertTrue(form.is_valid())

        # test missing username field
        form_data = {'password': 'password123'}
        form = LoginForm(data=form_data)
        self.assertFalse(form.is_valid())

        # test missing password field
        form_data = {'username': 'user123'}
        form = LoginForm(data=form_data)
        self.assertFalse(form.is_valid())

        # test empty username field
        form_data = {'username': '', 'password': 'password123'}
        form = LoginForm(data=form_data)
        self.assertFalse(form.is_valid())

        # test empty password field
        form_data = {'username': 'user123', 'password': ''}
        form = LoginForm(data=form_data)
        self.assertFalse(form.is_valid())
