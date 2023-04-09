from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User

from apps.invoice.views import InvoiceList


class TestInvoiceList(TestCase):
    def setUp(self):
        # create some test data
        self.user = User.objects.create_user(
            username='testuser', password='secret'
        )
        self.factory = RequestFactory()

    def test_url_redirects_anonymous_user(self):
        response = self.client.get("/invoice/")
        self.assertEqual(response.status_code, 302)

    def test_url_exists_at_correct_location(self):
        request = self.factory.get(reverse('invoice:invoice-list'))
        request.user = self.user
        response = InvoiceList.as_view()(request)
        self.assertEqual(response.status_code, 200)
