from unittest import TestCase, mock
import string
import random
from apps.utils.signals import generate_sku_num

class TestGenerateSkuNum(TestCase):

    def test_generates_sku_num(self):
        with mock.patch('random.choices', return_value=['A', 'B']) as mock_choices:
            sender = mock.Mock()
            sender.objects.filter.return_value.exists.return_value = False
            instance = mock.Mock(sku_num=None)
            k = 2
            generate_sku_num(sender, instance, k)
            mock_choices.assert_called_once_with(string.ascii_uppercase, k=k)  # change assertion
            sender.objects.filter.assert_called_once_with(sku_num=''.join(mock_choices.return_value))
            instance.sku_num = ''.join(mock_choices.return_value)
