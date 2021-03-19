from rest_framework.test import APITestCase, APIRequestFactory
from ...views import CreateItem, Item, Tax


class CreateItemTestCase(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = CreateItem.as_view()
        self.tax = Tax.create(0.23)

    def tests_create_item(self):
        request = self.factory.post('create_item', {'title': 'item title', 'name': 'item name', 'price': 12.34,
                                                    'earnings': 11.22, 'category': 1, 'subscription_term': 2,
                                                    'tax_value': 0.23}, format='json')
        response = self.view(request)
        item = Item.objects.get(pk=1)
        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(response.data['status'], 'OK')
        self.assertEqual(response.data['item']['title'], 'item title')
        self.assertEqual(response.data['item']['name'], 'item name')
        self.assertEqual(response.data['item']['price'], 12.34)
        self.assertEqual(response.data['item']['category'], 1)
        self.assertEqual(response.data['item']['earnings'], 11.22)
        self.assertEqual(response.data['item']['subscription_term'], 2)
        self.assertEqual(response.data['item']['vat']['tax_value'], 0.23)
        self.assertEqual(response.data['item']['ASIN'], item.ASIN)
        self.assertEqual(response.data['item']['title'], item.title)
        self.assertEqual(response.data['item']['name'], item.name)
        self.assertEqual(response.data['item']['price'], item.price)
        self.assertEqual(response.data['item']['category'], item.category)
        self.assertEqual(response.data['item']['earnings'], item.earnings)
        self.assertEqual(response.data['item']['subscription_term'], item.subscription_term)

    def test_create_item_with_wrong_tax_value(self):
        request = self.factory.post('create_item', {'title': 'item title', 'name': 'item name', 'price': 12.34,
                                                    'earnings': 11.22, 'category': 1, 'subscription_term': 2,
                                                    'tax_value': 0.24}, format='json')
        response = self.view(request)
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Tax with provided tax_value does not exist')

        request = self.factory.post('create_item', {'title': 'item title', 'name': 'item name', 'price': 12.34,
                                                    'earnings': 11.22, 'category': 1, 'subscription_term': 2,
                                                    'tax_value': 1.24}, format='json')
        response = self.view(request)
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Tax with provided tax_value does not exist')

        request = self.factory.post('create_item', {'title': 'item title', 'name': 'item name', 'price': 12.34,
                                                    'earnings': 11.22, 'category': 1, 'subscription_term': 2,
                                                    'tax_value': -0.24}, format='json')
        response = self.view(request)
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Tax with provided tax_value does not exist')

    def test_create_item_with_not_string_as_item_title(self):
        request = self.factory.post('create_item', {'title': 1, 'name': 'item name', 'price': 12.34, 'earnings': 11.22,
                                                    'category': 1, 'subscription_term': 2, 'tax_value': 0.23},
                                    format='json')
        response = self.view(request)
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Title error')

        request = self.factory.post('create_item', {'title': 0, 'name': 'item name', 'price': 12.34, 'earnings': 11.22,
                                                    'category': 1, 'subscription_term': 2, 'tax_value': 0.23},
                                    format='json')
        response = self.view(request)
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Title error')

        request = self.factory.post('create_item', {'title': -1, 'name': 'item name', 'price': 12.34, 'earnings': 11.22,
                                                    'category': 1, 'subscription_term': 2, 'tax_value': 0.23},
                                    format='json')
        response = self.view(request)
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Title error')

        request = self.factory.post('create_item', {'title': 1.1, 'name': 'item name', 'price': 12.34,
                                                    'earnings': 11.22, 'category': 1, 'subscription_term': 2,
                                                    'tax_value': 0.23}, format='json')
        response = self.view(request)
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Title error')

        request = self.factory.post('create_item', {'title': -1.1, 'name': 'item name', 'price': 12.34,
                                                    'earnings': 11.22, 'category': 1, 'subscription_term': 2,
                                                    'tax_value': 0.23}, format='json')
        response = self.view(request)
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Title error')

        request = self.factory.post('create_item', {'title': True, 'name': 'item name', 'price': 12.34,
                                                    'earnings': 11.22, 'category': 1, 'subscription_term': 2,
                                                    'tax_value': 0.23}, format='json')
        response = self.view(request)
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Title error')

        request = self.factory.post('create_item', {'title': False, 'name': 'item name', 'price': 12.34,
                                                    'earnings': 11.22, 'category': 1, 'subscription_term': 2,
                                                    'tax_value': 0.23}, format='json')
        response = self.view(request)
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Title error')

        request = self.factory.post('create_item', {'title': None, 'name': 'item name', 'price': 12.34,
                                                    'earnings': 11.22, 'category': 1, 'subscription_term': 2,
                                                    'tax_value': 0.23}, format='json')
        response = self.view(request)
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Title error')

        request = self.factory.post('create_item', {'title': list(), 'name': 'item name', 'price': 12.34,
                                                    'earnings': 11.22, 'category': 1, 'subscription_term': 2,
                                                    'tax_value': 0.23}, format='json')
        response = self.view(request)
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Title error')

        request = self.factory.post('create_item', {'title': tuple(), 'name': 'item name', 'price': 12.34,
                                                    'earnings': 11.22, 'category': 1, 'subscription_term': 2,
                                                    'tax_value': 0.23}, format='json')
        response = self.view(request)
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Title error')

        request = self.factory.post('create_item', {'title': dict(), 'name': 'item name', 'price': 12.34,
                                                    'earnings': 11.22, 'category': 1, 'subscription_term': 2,
                                                    'tax_value': 0.23}, format='json')
        response = self.view(request)
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Title error')

        request = self.factory.post('create_item', {'title': set(), 'name': 'item name', 'price': 12.34,
                                                    'earnings': 11.22, 'category': 1, 'subscription_term': 2,
                                                    'tax_value': 0.23}, format='json')
        response = self.view(request)
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Title error')

    def test_create_item_with_empty_string_as_title(self):
        request = self.factory.post('create_item', {'title': '', 'name': 'item name', 'price': 12.34,
                                                    'earnings': 11.22, 'category': 1, 'subscription_term': 2,
                                                    'tax_value': 0.23}, format='json')
        response = self.view(request)
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Title error')

        request = self.factory.post('create_item', {'title': ' ', 'name': 'item name', 'price': 12.34,
                                                    'earnings': 11.22, 'category': 1, 'subscription_term': 2,
                                                    'tax_value': 0.23}, format='json')
        response = self.view(request)
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Title error')

    def test_create_item_with_too_long_string_as_title(self):
        request = self.factory.post('create_item', {'title': '1' * 51, 'name': 'item name', 'price': 12.34,
                                                    'earnings': 11.22, 'category': 1, 'subscription_term': 2,
                                                    'tax_value': 0.23}, format='json')
        response = self.view(request)
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Title error')

    def test_create_item_with_not_string_as_item_name(self):
        request = self.factory.post('create_item', {'title': 'item title', 'name': 1, 'price': 12.34, 'earnings': 11.22,
                                                    'category': 1, 'subscription_term': 2, 'tax_value': 0.23},
                                    format='json')
        response = self.view(request)
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Name error')

        request = self.factory.post('create_item', {'title': 'item title', 'name': 0, 'price': 12.34, 'earnings': 11.22,
                                                    'category': 1, 'subscription_term': 2, 'tax_value': 0.23},
                                    format='json')
        response = self.view(request)
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Name error')

        request = self.factory.post('create_item', {'title': 'item title', 'name': -1, 'price': 12.34,
                                                    'earnings': 11.22, 'category': 1, 'subscription_term': 2,
                                                    'tax_value': 0.23}, format='json')
        response = self.view(request)
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Name error')

        request = self.factory.post('create_item', {'title': 'item title', 'name': 1.1, 'price': 12.34,
                                                    'earnings': 11.22, 'category': 1, 'subscription_term': 2,
                                                    'tax_value': 0.23}, format='json')
        response = self.view(request)
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Name error')

        request = self.factory.post('create_item', {'title': 'item title', 'name': -1.1, 'price': 12.34,
                                                    'earnings': 11.22, 'category': 1, 'subscription_term': 2,
                                                    'tax_value': 0.23}, format='json')
        response = self.view(request)
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Name error')

        request = self.factory.post('create_item', {'title': 'item title', 'name': True, 'price': 12.34,
                                                    'earnings': 11.22, 'category': 1, 'subscription_term': 2,
                                                    'tax_value': 0.23}, format='json')
        response = self.view(request)
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Name error')

        request = self.factory.post('create_item', {'title': 'item title', 'name': False, 'price': 12.34,
                                                    'earnings': 11.22, 'category': 1, 'subscription_term': 2,
                                                    'tax_value': 0.23}, format='json')
        response = self.view(request)
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Name error')

        request = self.factory.post('create_item', {'title': 'item title', 'name': None, 'price': 12.34,
                                                    'earnings': 11.22, 'category': 1, 'subscription_term': 2,
                                                    'tax_value': 0.23}, format='json')
        response = self.view(request)
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Name error')

        request = self.factory.post('create_item', {'title': 'item title', 'name': list(), 'price': 12.34,
                                                    'earnings': 11.22, 'category': 1, 'subscription_term': 2,
                                                    'tax_value': 0.23}, format='json')
        response = self.view(request)
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Name error')

        request = self.factory.post('create_item', {'title': 'item title', 'name': tuple(), 'price': 12.34,
                                                    'earnings': 11.22, 'category': 1, 'subscription_term': 2,
                                                    'tax_value': 0.23}, format='json')
        response = self.view(request)
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Name error')

        request = self.factory.post('create_item', {'title': 'item title', 'name': dict(), 'price': 12.34,
                                                    'earnings': 11.22, 'category': 1, 'subscription_term': 2,
                                                    'tax_value': 0.23}, format='json')
        response = self.view(request)
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Name error')

        request = self.factory.post('create_item', {'title': 'item title', 'name': set(), 'price': 12.34,
                                                    'earnings': 11.22, 'category': 1, 'subscription_term': 2,
                                                    'tax_value': 0.23}, format='json')
        response = self.view(request)
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Name error')

    def test_create_item_with_empty_string_as_name(self):
        request = self.factory.post('create_item', {'title': 'item title', 'name': '', 'price': 12.34,
                                                    'earnings': 11.22, 'category': 1, 'subscription_term': 2,
                                                    'tax_value': 0.23}, format='json')
        response = self.view(request)
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Name error')

        request = self.factory.post('create_item', {'title': 'item title', 'name': ' ', 'price': 12.34,
                                                    'earnings': 11.22, 'category': 1, 'subscription_term': 2,
                                                    'tax_value': 0.23}, format='json')
        response = self.view(request)
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Name error')

    def test_create_item_with_too_long_string_as_name(self):
        request = self.factory.post('create_item', {'title': 'item title', 'name': '1' * 51, 'price': 12.34,
                                                    'earnings': 11.22, 'category': 1, 'subscription_term': 2,
                                                    'tax_value': 0.23}, format='json')
        response = self.view(request)
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Name error')

    def test_create_item_with_not_int_or_float_as_price(self):
        request = self.factory.post('create_item', {'title': 'item title', 'name': 'item name', 'price': '',
                                                    'earnings': 11.22, 'category': 1, 'subscription_term': 2,
                                                    'tax_value': 0.23}, format='json')
        response = self.view(request)
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Price error')

        request = self.factory.post('create_item', {'title': 'item title', 'name': 'item name', 'price': ' ',
                                                    'earnings': 11.22, 'category': 1, 'subscription_term': 2,
                                                    'tax_value': 0.23}, format='json')
        response = self.view(request)
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Price error')

        request = self.factory.post('create_item', {'title': 'item title', 'name': 'item name', 'price': '1',
                                                    'earnings': 11.22, 'category': 1, 'subscription_term': 2,
                                                    'tax_value': 0.23}, format='json')
        response = self.view(request)
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Price error')

        request = self.factory.post('create_item', {'title': 'item title', 'name': 'item name', 'price': '0',
                                                    'earnings': 11.22, 'category': 1, 'subscription_term': 2,
                                                    'tax_value': 0.23}, format='json')
        response = self.view(request)
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Price error')

        request = self.factory.post('create_item', {'title': 'item title', 'name': 'item name', 'price': '-1',
                                                    'earnings': 11.22, 'category': 1, 'subscription_term': 2,
                                                    'tax_value': 0.23}, format='json')
        response = self.view(request)
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Price error')

        request = self.factory.post('create_item', {'title': 'item title', 'name': 'item name', 'price': '1.1',
                                                    'earnings': 11.22, 'category': 1, 'subscription_term': 2,
                                                    'tax_value': 0.23}, format='json')
        response = self.view(request)
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Price error')

        request = self.factory.post('create_item', {'title': 'item title', 'name': 'item name', 'price': '-1.1',
                                                    'earnings': 11.22, 'category': 1, 'subscription_term': 2,
                                                    'tax_value': 0.23}, format='json')
        response = self.view(request)
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Price error')

        request = self.factory.post('create_item', {'title': 'item title', 'name': 'item name', 'price': 'Text',
                                                    'earnings': 11.22, 'category': 1, 'subscription_term': 2,
                                                    'tax_value': 0.23}, format='json')
        response = self.view(request)
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Price error')

        request = self.factory.post('create_item', {'title': 'item title', 'name': 'item name', 'price': True,
                                                    'earnings': 11.22, 'category': 1, 'subscription_term': 2,
                                                    'tax_value': 0.23}, format='json')
        response = self.view(request)
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Price error')

        request = self.factory.post('create_item', {'title': 'item title', 'name': 'item name', 'price': False,
                                                    'earnings': 11.22, 'category': 1, 'subscription_term': 2,
                                                    'tax_value': 0.23}, format='json')
        response = self.view(request)
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Price error')

        request = self.factory.post('create_item', {'title': 'item title', 'name': 'item name', 'price': None,
                                                    'earnings': 11.22, 'category': 1, 'subscription_term': 2,
                                                    'tax_value': 0.23}, format='json')
        response = self.view(request)
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Price error')

        request = self.factory.post('create_item', {'title': 'item title', 'name': 'item name', 'price': list(),
                                                    'earnings': 11.22, 'category': 1, 'subscription_term': 2,
                                                    'tax_value': 0.23}, format='json')
        response = self.view(request)
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Price error')

        request = self.factory.post('create_item', {'title': 'item title', 'name': 'item name', 'price': dict(),
                                                    'earnings': 11.22, 'category': 1, 'subscription_term': 2,
                                                    'tax_value': 0.23}, format='json')
        response = self.view(request)
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Price error')

        request = self.factory.post('create_item', {'title': 'item title', 'name': 'item name', 'price': set(),
                                                    'earnings': 11.22, 'category': 1, 'subscription_term': 2,
                                                    'tax_value': 0.23}, format='json')
        response = self.view(request)
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Price error')

    def test_create_item_with_negative_int_or_float_as_price(self):
        request = self.factory.post('create_item', {'title': 'item title', 'name': 'item name', 'price': -1,
                                                    'earnings': 11.22, 'category': 1, 'subscription_term': 2,
                                                    'tax_value': 0.23}, format='json')
        response = self.view(request)
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Price error, Earnings error')

        request = self.factory.post('create_item', {'title': 'item title', 'name': 'item name', 'price': -1.1,
                                                    'earnings': 11.22, 'category': 1, 'subscription_term': 2,
                                                    'tax_value': 0.23}, format='json')
        response = self.view(request)
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Price error, Earnings error')

    def test_create_item_with_0_as_price(self):
        request = self.factory.post('create_item', {'title': 'item title', 'name': 'item name', 'price': 0,
                                                    'earnings': 11.22, 'category': 1, 'subscription_term': 2,
                                                    'tax_value': 0.23}, format='json')
        response = self.view(request)
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Price error, Earnings error')

    def test_create_item_with_not_int_or_float_as_earnings(self):
        request = self.factory.post('create_item', {'title': 'item title', 'name': 'item name', 'price': 12.34,
                                                    'earnings': '', 'category': 1, 'subscription_term': 2,
                                                    'tax_value': 0.23}, format='json')
        response = self.view(request)
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Earnings error')

        request = self.factory.post('create_item', {'title': 'item title', 'name': 'item name', 'price': 12.34,
                                                    'earnings': ' ', 'category': 1, 'subscription_term': 2,
                                                    'tax_value': 0.23}, format='json')
        response = self.view(request)
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Earnings error')

        request = self.factory.post('create_item', {'title': 'item title', 'name': 'item name', 'price': 12.34,
                                                    'earnings': '1', 'category': 1, 'subscription_term': 2,
                                                    'tax_value': 0.23}, format='json')
        response = self.view(request)
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Earnings error')

        request = self.factory.post('create_item', {'title': 'item title', 'name': 'item name', 'price': 12.34,
                                                    'earnings': '0', 'category': 1, 'subscription_term': 2,
                                                    'tax_value': 0.23}, format='json')
        response = self.view(request)
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Earnings error')

        request = self.factory.post('create_item', {'title': 'item title', 'name': 'item name', 'price': 12.34,
                                                    'earnings': '-1', 'category': 1, 'subscription_term': 2,
                                                    'tax_value': 0.23}, format='json')
        response = self.view(request)
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Earnings error')

        request = self.factory.post('create_item', {'title': 'item title', 'name': 'item name', 'price': 12.34,
                                                    'earnings': '1.1', 'category': 1, 'subscription_term': 2,
                                                    'tax_value': 0.23}, format='json')
        response = self.view(request)
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Earnings error')

        request = self.factory.post('create_item', {'title': 'item title', 'name': 'item name', 'price': 12.34,
                                                    'earnings': '-1.1', 'category': 1, 'subscription_term': 2,
                                                    'tax_value': 0.23}, format='json')
        response = self.view(request)
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Earnings error')

        request = self.factory.post('create_item', {'title': 'item title', 'name': 'item name', 'price': 12.34,
                                                    'earnings': 'Text', 'category': 1, 'subscription_term': 2,
                                                    'tax_value': 0.23}, format='json')
        response = self.view(request)
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Earnings error')

        request = self.factory.post('create_item', {'title': 'item title', 'name': 'item name', 'price': 12.34,
                                                    'earnings': True, 'category': 1, 'subscription_term': 2,
                                                    'tax_value': 0.23}, format='json')
        response = self.view(request)
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Earnings error')

        request = self.factory.post('create_item', {'title': 'item title', 'name': 'item name', 'price': 12.34,
                                                    'earnings': False, 'category': 1, 'subscription_term': 2,
                                                    'tax_value': 0.23}, format='json')
        response = self.view(request)
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Earnings error')

        request = self.factory.post('create_item', {'title': 'item title', 'name': 'item name', 'price': 12.34,
                                                    'earnings': None, 'category': 1, 'subscription_term': 2,
                                                    'tax_value': 0.23}, format='json')
        response = self.view(request)
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Earnings error')

        request = self.factory.post('create_item', {'title': 'item title', 'name': 'item name', 'price': 12.34,
                                                    'earnings': list(), 'category': 1, 'subscription_term': 2,
                                                    'tax_value': 0.23}, format='json')
        response = self.view(request)
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Earnings error')

        request = self.factory.post('create_item', {'title': 'item title', 'name': 'item name', 'price': 12.34,
                                                    'earnings': tuple(), 'category': 1, 'subscription_term': 2,
                                                    'tax_value': 0.23}, format='json')
        response = self.view(request)
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Earnings error')

        request = self.factory.post('create_item', {'title': 'item title', 'name': 'item name', 'price': 12.34,
                                                    'earnings': dict(), 'category': 1, 'subscription_term': 2,
                                                    'tax_value': 0.23}, format='json')
        response = self.view(request)
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Earnings error')

        request = self.factory.post('create_item', {'title': 'item title', 'name': 'item name', 'price': 12.34,
                                                    'earnings': set(), 'category': 1, 'subscription_term': 2,
                                                    'tax_value': 0.23}, format='json')
        response = self.view(request)
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Earnings error')

    def test_create_item_with_earnings_higher_than_price(self):
        request = self.factory.post('create_item', {'title': 'item title', 'name': 'item name', 'price': 12.34,
                                                    'earnings': 15, 'category': 1, 'subscription_term': 2,
                                                    'tax_value': 0.23}, format='json')
        response = self.view(request)
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Earnings error')

        request = self.factory.post('create_item', {'title': 'item title', 'name': 'item name', 'price': 12.34,
                                                    'earnings': 15.1, 'category': 1, 'subscription_term': 2,
                                                    'tax_value': 0.23}, format='json')
        response = self.view(request)
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Earnings error')

    def test_create_item_with_negative_int_or_float_as_earnings(self):
        request = self.factory.post('create_item', {'title': 'item title', 'name': 'item name', 'price': 12.34,
                                                    'earnings': -1, 'category': 1, 'subscription_term': 2,
                                                    'tax_value': 0.23}, format='json')
        response = self.view(request)
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Earnings error')

        request = self.factory.post('create_item', {'title': 'item title', 'name': 'item name', 'price': 12.34,
                                                    'earnings': -1.1, 'category': 1, 'subscription_term': 2,
                                                    'tax_value': 0.23}, format='json')
        response = self.view(request)
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Earnings error')

    def test_create_item_with_0_as_earnings(self):
        request = self.factory.post('create_item', {'title': 'item title', 'name': 'item name', 'price': 12.34,
                                                    'earnings': 0, 'category': 1, 'subscription_term': 2,
                                                    'tax_value': 0.23}, format='json')
        response = self.view(request)
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Earnings error')

    def test_create_item_with_0_as_earnings_and_price(self):
        request = self.factory.post('create_item', {'title': 'item title', 'name': 'item name', 'price': 0,
                                                    'earnings': 0, 'category': 1, 'subscription_term': 2,
                                                    'tax_value': 0.23}, format='json')
        response = self.view(request)
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Price error, Earnings error')

    def test_create_item_with_not_int_or_none_as_category(self):
        request = self.factory.post('create_item', {'title': 'item title', 'name': 'item name', 'price': 12.34,
                                                    'earnings': 11.22, 'category': '', 'subscription_term': 2,
                                                    'tax_value': 0.23}, format='json')
        response = self.view(request)
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Category error')

        request = self.factory.post('create_item', {'title': 'item title', 'name': 'item name', 'price': 12.34,
                                                    'earnings': 11.22, 'category': ' ', 'subscription_term': 2,
                                                    'tax_value': 0.23}, format='json')
        response = self.view(request)
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Category error')

        request = self.factory.post('create_item', {'title': 'item title', 'name': 'item name', 'price': 12.34,
                                                    'earnings': 11.22, 'category': '1', 'subscription_term': 2,
                                                    'tax_value': 0.23}, format='json')
        response = self.view(request)
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Category error')

        request = self.factory.post('create_item', {'title': 'item title', 'name': 'item name', 'price': 12.34,
                                                    'earnings': 11.22, 'category': '0', 'subscription_term': 2,
                                                    'tax_value': 0.23}, format='json')
        response = self.view(request)
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Category error')

        request = self.factory.post('create_item', {'title': 'item title', 'name': 'item name', 'price': 12.34,
                                                    'earnings': 11.22, 'category': '-1', 'subscription_term': 2,
                                                    'tax_value': 0.23}, format='json')
        response = self.view(request)
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Category error')

        request = self.factory.post('create_item', {'title': 'item title', 'name': 'item name', 'price': 12.34,
                                                    'earnings': 11.22, 'category': '1.1', 'subscription_term': 2,
                                                    'tax_value': 0.23}, format='json')
        response = self.view(request)
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Category error')

        request = self.factory.post('create_item', {'title': 'item title', 'name': 'item name', 'price': 12.34,
                                                    'earnings': 11.22, 'category': '-1.1', 'subscription_term': 2,
                                                    'tax_value': 0.23}, format='json')
        response = self.view(request)
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Category error')

        request = self.factory.post('create_item', {'title': 'item title', 'name': 'item name', 'price': 12.34,
                                                    'earnings': 11.22, 'category': 'Text', 'subscription_term': 2,
                                                    'tax_value': 0.23}, format='json')
        response = self.view(request)
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Category error')

        request = self.factory.post('create_item', {'title': 'item title', 'name': 'item name', 'price': 12.34,
                                                    'earnings': 11.22, 'category': 'Subscription',
                                                    'subscription_term': 2, 'tax_value': 0.23}, format='json')
        response = self.view(request)
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Category error')

        request = self.factory.post('create_item', {'title': 'item title', 'name': 'item name', 'price': 12.34,
                                                    'earnings': 11.22, 'category': 1.1, 'subscription_term': 2,
                                                    'tax_value': 0.23}, format='json')
        response = self.view(request)
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Category error')

        request = self.factory.post('create_item', {'title': 'item title', 'name': 'item name', 'price': 12.34,
                                                    'earnings': 11.22, 'category': -1.1, 'subscription_term': 2,
                                                    'tax_value': 0.23}, format='json')
        response = self.view(request)
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Category error')

        request = self.factory.post('create_item', {'title': 'item title', 'name': 'item name', 'price': 12.34,
                                                    'earnings': 11.22, 'category': True, 'subscription_term': 2,
                                                    'tax_value': 0.23}, format='json')
        response = self.view(request)
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Category error')

        request = self.factory.post('create_item', {'title': 'item title', 'name': 'item name', 'price': 12.34,
                                                    'earnings': 11.22, 'category': False, 'subscription_term': 2,
                                                    'tax_value': 0.23}, format='json')
        response = self.view(request)
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Category error')

        request = self.factory.post('create_item', {'title': 'item title', 'name': 'item name', 'price': 12.34,
                                                    'earnings': 11.22, 'category': list(), 'subscription_term': 2,
                                                    'tax_value': 0.23}, format='json')
        response = self.view(request)
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Category error')

        request = self.factory.post('create_item', {'title': 'item title', 'name': 'item name', 'price': 12.34,
                                                    'earnings': 11.22, 'category': tuple(), 'subscription_term': 2,
                                                    'tax_value': 0.23}, format='json')
        response = self.view(request)
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Category error')

        request = self.factory.post('create_item', {'title': 'item title', 'name': 'item name', 'price': 12.34,
                                                    'earnings': 11.22, 'category': dict(), 'subscription_term': 2,
                                                    'tax_value': 0.23}, format='json')
        response = self.view(request)
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Category error')

        request = self.factory.post('create_item', {'title': 'item title', 'name': 'item name', 'price': 12.34,
                                                    'earnings': 11.22, 'category': set(), 'subscription_term': 2,
                                                    'tax_value': 0.23}, format='json')
        response = self.view(request)
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Category error')

    def test_create_item_with_category_out_of_range(self):
        request = self.factory.post('create_item', {'title': 'item title', 'name': 'item name', 'price': 12.34,
                                                    'earnings': 11.22, 'category': 0, 'subscription_term': 2,
                                                    'tax_value': 0.23}, format='json')
        response = self.view(request)
        item = Item.objects.get(pk=1)
        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(response.data['status'], 'OK')
        self.assertEqual(response.data['item']['title'], 'item title')
        self.assertEqual(response.data['item']['name'], 'item name')
        self.assertEqual(response.data['item']['price'], 12.34)
        self.assertEqual(response.data['item']['category'], None)
        self.assertEqual(response.data['item']['earnings'], 11.22)
        self.assertEqual(response.data['item']['subscription_term'], None)
        self.assertEqual(response.data['item']['vat']['tax_value'], 0.23)
        self.assertEqual(response.data['item']['ASIN'], item.ASIN)
        self.assertEqual(response.data['item']['title'], item.title)
        self.assertEqual(response.data['item']['name'], item.name)
        self.assertEqual(response.data['item']['price'], item.price)
        self.assertEqual(response.data['item']['category'], item.category)
        self.assertEqual(response.data['item']['earnings'], item.earnings)
        self.assertEqual(response.data['item']['subscription_term'], item.subscription_term)

        request = self.factory.post('create_item', {'title': 'item title', 'name': 'item name', 'price': 12.34,
                                                    'earnings': 11.22, 'category': 6, 'subscription_term': 2,
                                                    'tax_value': 0.23}, format='json')
        response = self.view(request)
        item = Item.objects.get(pk=2)
        self.assertEqual(Item.objects.count(), 2)
        self.assertEqual(response.data['status'], 'OK')
        self.assertEqual(response.data['item']['title'], 'item title')
        self.assertEqual(response.data['item']['name'], 'item name')
        self.assertEqual(response.data['item']['price'], 12.34)
        self.assertEqual(response.data['item']['category'], None)
        self.assertEqual(response.data['item']['earnings'], 11.22)
        self.assertEqual(response.data['item']['subscription_term'], None)
        self.assertEqual(response.data['item']['vat']['tax_value'], 0.23)
        self.assertEqual(response.data['item']['ASIN'], item.ASIN)
        self.assertEqual(response.data['item']['title'], item.title)
        self.assertEqual(response.data['item']['name'], item.name)
        self.assertEqual(response.data['item']['price'], item.price)
        self.assertEqual(response.data['item']['category'], item.category)
        self.assertEqual(response.data['item']['earnings'], item.earnings)
        self.assertEqual(response.data['item']['subscription_term'], item.subscription_term)

    def test_create_item_with_not_float_as_subscription_term(self):
        request = self.factory.post('create_item', {'title': 'item title', 'name': 'item name', 'price': 12.34,
                                                    'earnings': 11.22, 'category': 1, 'subscription_term': '',
                                                    'tax_value': 0.23}, format='json')
        response = self.view(request)
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Subscription term error')

        request = self.factory.post('create_item', {'title': 'item title', 'name': 'item name', 'price': 12.34,
                                                    'earnings': 11.22, 'category': 1, 'subscription_term': ' ',
                                                    'tax_value': 0.23}, format='json')
        response = self.view(request)
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Subscription term error')

        request = self.factory.post('create_item', {'title': 'item title', 'name': 'item name', 'price': 12.34,
                                                    'earnings': 11.22, 'category': 1, 'subscription_term': '1',
                                                    'tax_value': 0.23}, format='json')
        response = self.view(request)
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Subscription term error')

        request = self.factory.post('create_item', {'title': 'item title', 'name': 'item name', 'price': 12.34,
                                                    'earnings': 11.22, 'category': 1, 'subscription_term': '0',
                                                    'tax_value': 0.23}, format='json')
        response = self.view(request)
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Subscription term error')

        request = self.factory.post('create_item', {'title': 'item title', 'name': 'item name', 'price': 12.34,
                                                    'earnings': 11.22, 'category': 1, 'subscription_term': '-1',
                                                    'tax_value': 0.23}, format='json')
        response = self.view(request)
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Subscription term error')

        request = self.factory.post('create_item', {'title': 'item title', 'name': 'item name', 'price': 12.34,
                                                    'earnings': 11.22, 'category': 1, 'subscription_term': '1.1',
                                                    'tax_value': 0.23}, format='json')
        response = self.view(request)
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Subscription term error')

        request = self.factory.post('create_item', {'title': 'item title', 'name': 'item name', 'price': 12.34,
                                                    'earnings': 11.22, 'category': 1, 'subscription_term': '-1.1',
                                                    'tax_value': 0.23}, format='json')
        response = self.view(request)
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Subscription term error')

        request = self.factory.post('create_item', {'title': 'item title', 'name': 'item name', 'price': 12.34,
                                                    'earnings': 11.22, 'category': 1, 'subscription_term': 'Text',
                                                    'tax_value': 0.23}, format='json')
        response = self.view(request)
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Subscription term error')

        request = self.factory.post('create_item', {'title': 'item title', 'name': 'item name', 'price': 12.34,
                                                    'earnings': 11.22, 'category': 1, 'subscription_term': 'weekly',
                                                    'tax_value': 0.23}, format='json')
        response = self.view(request)
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Subscription term error')

    def test_create_item_with_subscription_term_out_of_range(self):
        request = self.factory.post('create_item', {'title': 'item title', 'name': 'item name', 'price': 12.34,
                                                    'earnings': 11.22, 'category': 1, 'subscription_term': 0,
                                                    'tax_value': 0.23}, format='json')
        response = self.view(request)
        item = Item.objects.get(pk=1)
        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(response.data['status'], 'OK')
        self.assertEqual(response.data['item']['title'], 'item title')
        self.assertEqual(response.data['item']['name'], 'item name')
        self.assertEqual(response.data['item']['price'], 12.34)
        self.assertEqual(response.data['item']['category'], 1)
        self.assertEqual(response.data['item']['earnings'], 11.22)
        self.assertEqual(response.data['item']['subscription_term'], 1)
        self.assertEqual(response.data['item']['vat']['tax_value'], 0.23)
        self.assertEqual(response.data['item']['ASIN'], item.ASIN)
        self.assertEqual(response.data['item']['title'], item.title)
        self.assertEqual(response.data['item']['name'], item.name)
        self.assertEqual(response.data['item']['price'], item.price)
        self.assertEqual(response.data['item']['category'], item.category)
        self.assertEqual(response.data['item']['earnings'], item.earnings)
        self.assertEqual(response.data['item']['subscription_term'], item.subscription_term)

        request = self.factory.post('create_item', {'title': 'item title', 'name': 'item name', 'price': 12.34,
                                                    'earnings': 11.22, 'category': 1, 'subscription_term': 8,
                                                    'tax_value': 0.23}, format='json')
        response = self.view(request)
        item = Item.objects.get(pk=2)
        self.assertEqual(Item.objects.count(), 2)
        self.assertEqual(response.data['status'], 'OK')
        self.assertEqual(response.data['item']['title'], 'item title')
        self.assertEqual(response.data['item']['name'], 'item name')
        self.assertEqual(response.data['item']['price'], 12.34)
        self.assertEqual(response.data['item']['category'], 1)
        self.assertEqual(response.data['item']['earnings'], 11.22)
        self.assertEqual(response.data['item']['subscription_term'], 1)
        self.assertEqual(response.data['item']['vat']['tax_value'], 0.23)
        self.assertEqual(response.data['item']['ASIN'], item.ASIN)
        self.assertEqual(response.data['item']['title'], item.title)
        self.assertEqual(response.data['item']['name'], item.name)
        self.assertEqual(response.data['item']['price'], item.price)
        self.assertEqual(response.data['item']['category'], item.category)
        self.assertEqual(response.data['item']['earnings'], item.earnings)
        self.assertEqual(response.data['item']['subscription_term'], item.subscription_term)

    def test_create_item_with_not_float_as_tax_value(self):
        request = self.factory.post('create_item', {'title': 'item title', 'name': 'item name', 'price': 12.34,
                                                    'earnings': 11.22, 'category': 1, 'subscription_term': '',
                                                    'tax_value': ''}, format='json')
        response = self.view(request)
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Tax_value error')

        request = self.factory.post('create_item', {'title': 'item title', 'name': 'item name', 'price': 12.34,
                                                    'earnings': 11.22, 'category': 1, 'subscription_term': '',
                                                    'tax_value': ' '}, format='json')
        response = self.view(request)
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Tax_value error')

        request = self.factory.post('create_item', {'title': 'item title', 'name': 'item name', 'price': 12.34,
                                                    'earnings': 11.22, 'category': 1, 'subscription_term': '',
                                                    'tax_value': '1'}, format='json')
        response = self.view(request)
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Tax_value error')

        request = self.factory.post('create_item', {'title': 'item title', 'name': 'item name', 'price': 12.34,
                                                    'earnings': 11.22, 'category': 1, 'subscription_term': '',
                                                    'tax_value': '0'}, format='json')
        response = self.view(request)
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Tax_value error')

        request = self.factory.post('create_item', {'title': 'item title', 'name': 'item name', 'price': 12.34,
                                                    'earnings': 11.22, 'category': 1, 'subscription_term': '',
                                                    'tax_value': '-1'}, format='json')
        response = self.view(request)
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Tax_value error')

        request = self.factory.post('create_item', {'title': 'item title', 'name': 'item name', 'price': 12.34,
                                                    'earnings': 11.22, 'category': 1, 'subscription_term': '',
                                                    'tax_value': '1.1'}, format='json')
        response = self.view(request)
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Tax_value error')

        request = self.factory.post('create_item', {'title': 'item title', 'name': 'item name', 'price': 12.34,
                                                    'earnings': 11.22, 'category': 1, 'subscription_term': '',
                                                    'tax_value': '-1.1'}, format='json')
        response = self.view(request)
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Tax_value error')

        request = self.factory.post('create_item', {'title': 'item title', 'name': 'item name', 'price': 12.34,
                                                    'earnings': 11.22, 'category': 1, 'subscription_term': '',
                                                    'tax_value': '0.23'}, format='json')
        response = self.view(request)
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Tax_value error')

        request = self.factory.post('create_item', {'title': 'item title', 'name': 'item name', 'price': 12.34,
                                                    'earnings': 11.22, 'category': 1, 'subscription_term': '',
                                                    'tax_value': 'Text'}, format='json')
        response = self.view(request)
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Tax_value error')

        request = self.factory.post('create_item', {'title': 'item title', 'name': 'item name', 'price': 12.34,
                                                    'earnings': 11.22, 'category': 1, 'subscription_term': '',
                                                    'tax_value': 1}, format='json')
        response = self.view(request)
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Tax with provided tax_value does not exist')

        request = self.factory.post('create_item', {'title': 'item title', 'name': 'item name', 'price': 12.34,
                                                    'earnings': 11.22, 'category': 1, 'subscription_term': '',
                                                    'tax_value': 0}, format='json')
        response = self.view(request)
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Tax with provided tax_value does not exist')

        request = self.factory.post('create_item', {'title': 'item title', 'name': 'item name', 'price': 12.34,
                                                    'earnings': 11.22, 'category': 1, 'subscription_term': '',
                                                    'tax_value': -1}, format='json')
        response = self.view(request)
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Tax with provided tax_value does not exist')

        request = self.factory.post('create_item', {'title': 'item title', 'name': 'item name', 'price': 12.34,
                                                    'earnings': 11.22, 'category': 1, 'subscription_term': '',
                                                    'tax_value': True}, format='json')
        response = self.view(request)
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Tax_value error')

        request = self.factory.post('create_item', {'title': 'item title', 'name': 'item name', 'price': 12.34,
                                                    'earnings': 11.22, 'category': 1, 'subscription_term': '',
                                                    'tax_value': False}, format='json')
        response = self.view(request)
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Tax_value error')

        request = self.factory.post('create_item', {'title': 'item title', 'name': 'item name', 'price': 12.34,
                                                    'earnings': 11.22, 'category': 1, 'subscription_term': '',
                                                    'tax_value': None}, format='json')
        response = self.view(request)
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Tax_value error')

        request = self.factory.post('create_item', {'title': 'item title', 'name': 'item name', 'price': 12.34,
                                                    'earnings': 11.22, 'category': 1, 'subscription_term': '',
                                                    'tax_value': list()}, format='json')
        response = self.view(request)
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Tax_value error')

        request = self.factory.post('create_item', {'title': 'item title', 'name': 'item name', 'price': 12.34,
                                                    'earnings': 11.22, 'category': 1, 'subscription_term': '',
                                                    'tax_value': tuple()}, format='json')
        response = self.view(request)
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Tax_value error')

        request = self.factory.post('create_item', {'title': 'item title', 'name': 'item name', 'price': 12.34,
                                                    'earnings': 11.22, 'category': 1, 'subscription_term': '',
                                                    'tax_value': dict()}, format='json')
        response = self.view(request)
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Tax_value error')

        request = self.factory.post('create_item', {'title': 'item title', 'name': 'item name', 'price': 12.34,
                                                    'earnings': 11.22, 'category': 1, 'subscription_term': '',
                                                    'tax_value': set()}, format='json')
        response = self.view(request)
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Tax_value error')

    def test_create_item_with_missing_arguments(self):
        request = self.factory.post('create_item', {'name': 'item name', 'price': 12.34, 'earnings': 11.22,
                                                    'category': 1, 'subscription_term': 2, 'tax_value': 0.23},
                                    format='json')
        response = self.view(request)
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'missing 1 required positional argument: \'title\'')

        request = self.factory.post('create_item', {'title': 'item title', 'price': 12.34, 'earnings': 11.22,
                                                    'category': 1, 'subscription_term': 2, 'tax_value': 0.23},
                                    format='json')
        response = self.view(request)
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'missing 1 required positional argument: \'name\'')

        request = self.factory.post('create_item', {'title': 'item title', 'name': 'item name', 'earnings': 11.22,
                                                    'category': 1, 'subscription_term': 2, 'tax_value': 0.23},
                                    format='json')
        response = self.view(request)
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'missing 1 required positional argument: \'price\'')

        request = self.factory.post('create_item', {'title': 'item title', 'name': 'item name', 'price': 12.34,
                                                    'category': 1, 'subscription_term': 2, 'tax_value': 0.23},
                                    format='json')
        response = self.view(request)
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'missing 1 required positional argument: \'earnings\'')

        request = self.factory.post('create_item', {'title': 'item title', 'name': 'item name', 'price': 12.34,
                                                    'earnings': 11.22, 'subscription_term': 2, 'tax_value': 0.23},
                                    format='json')
        response = self.view(request)
        item = Item.objects.get(pk=1)
        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(response.data['status'], 'OK')
        self.assertEqual(response.data['item']['title'], 'item title')
        self.assertEqual(response.data['item']['name'], 'item name')
        self.assertEqual(response.data['item']['price'], 12.34)
        self.assertEqual(response.data['item']['category'], None)
        self.assertEqual(response.data['item']['earnings'], 11.22)
        self.assertEqual(response.data['item']['subscription_term'], None)
        self.assertEqual(response.data['item']['vat']['tax_value'], 0.23)
        self.assertEqual(response.data['item']['ASIN'], item.ASIN)
        self.assertEqual(response.data['item']['title'], item.title)
        self.assertEqual(response.data['item']['name'], item.name)
        self.assertEqual(response.data['item']['price'], item.price)
        self.assertEqual(response.data['item']['category'], item.category)
        self.assertEqual(response.data['item']['earnings'], item.earnings)
        self.assertEqual(response.data['item']['subscription_term'], item.subscription_term)

        request = self.factory.post('create_item', {'title': 'item title', 'name': 'item name', 'price': 12.34,
                                                    'earnings': 11.22, 'category': 1, 'tax_value': 0.23}, format='json')
        response = self.view(request)
        item = Item.objects.get(pk=2)
        self.assertEqual(Item.objects.count(), 2)
        self.assertEqual(response.data['status'], 'OK')
        self.assertEqual(response.data['item']['title'], 'item title')
        self.assertEqual(response.data['item']['name'], 'item name')
        self.assertEqual(response.data['item']['price'], 12.34)
        self.assertEqual(response.data['item']['category'], 1)
        self.assertEqual(response.data['item']['earnings'], 11.22)
        self.assertEqual(response.data['item']['subscription_term'], 1)
        self.assertEqual(response.data['item']['vat']['tax_value'], 0.23)
        self.assertEqual(response.data['item']['ASIN'], item.ASIN)
        self.assertEqual(response.data['item']['title'], item.title)
        self.assertEqual(response.data['item']['name'], item.name)
        self.assertEqual(response.data['item']['price'], item.price)
        self.assertEqual(response.data['item']['category'], item.category)
        self.assertEqual(response.data['item']['earnings'], item.earnings)
        self.assertEqual(response.data['item']['subscription_term'], item.subscription_term)

        request = self.factory.post('create_item', {'title': 'item title', 'name': 'item name', 'price': 12.34,
                                                    'earnings': 11.22, 'category': 1, 'subscription_term': 2},
                                    format='json')
        response = self.view(request)
        self.assertEqual(Item.objects.count(), 2)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'missing argument: tax_value')
