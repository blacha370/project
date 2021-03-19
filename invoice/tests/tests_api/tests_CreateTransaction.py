from rest_framework.test import APITestCase, APIRequestFactory
from ...views import CreateTransaction, Transaction, Item, SoldItem, Tax, Marketplace, Company, Customer, Address


class CreateTransactionTestCase(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = CreateTransaction.as_view()
        address = Address.create(country='Country', city='City', postal_code='11-222', street='Street',
                                 building_number=1)
        self.company = Company.create(name='Company', address=address)
        address = Address.create(country='Country', city='City', postal_code='11-222', street='Street',
                                 building_number=2)
        self.customer = Customer.create(name='Customer', address=address)
        taxes = []
        for tax in (0.00, 0.05, 0.08, 0.23):
            taxes.append(Tax.create(tax_value=tax))
        for i in range(4):
            Item.create(title='Title {}'.format(i), name='Name {}'.format(i), price=12.34, earnings=11.22,
                        vat=taxes[i])
        self.items = Item.objects.all()
        self.marketplace = Marketplace()
        self.marketplace.save()

    def test_create_transaction(self):
        items = [{'ASIN': item.ASIN, 'count': 10} for item in self.items]
        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 1)
        self.assertEqual(SoldItem.objects.count(), 4)
        self.assertEqual(response.data['status'], 'OK')
        self.assertEqual(response.data['transaction']['vendor']['SKU'], self.company.SKU)
        self.assertEqual(response.data['transaction']['customer']['app_id'], self.customer.app_id)
        self.assertEqual(response.data['transaction']['marketplace']['name'], self.marketplace.name)
        self.assertFalse(response.data['transaction']['refund'])

    def test_create_second_transaction(self):
        items = [{'ASIN': item.ASIN, 'count': 10} for item in self.items]
        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items}, format='json')
        response = self.view(request)
        transaction = Transaction.objects.get(pk=1)
        self.assertEqual(Transaction.objects.count(), 1)
        self.assertEqual(SoldItem.objects.count(), 4)
        self.assertEqual(response.data['status'], 'OK')
        self.assertEqual(response.data['transaction']['vendor']['SKU'], self.company.SKU)
        self.assertEqual(response.data['transaction']['customer']['app_id'], self.customer.app_id)
        self.assertEqual(response.data['transaction']['marketplace']['name'], self.marketplace.name)

        items = [{'ASIN': item.ASIN, 'count': 10} for item in self.items]
        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items}, format='json')
        response = self.view(request)
        second_transaction = Transaction.objects.get(pk=2)
        self.assertNotEqual(transaction, second_transaction)
        self.assertEqual(Transaction.objects.count(), 2)
        self.assertEqual(SoldItem.objects.count(), 8)
        self.assertEqual(response.data['status'], 'OK')
        self.assertEqual(response.data['transaction']['vendor']['SKU'], self.company.SKU)
        self.assertEqual(response.data['transaction']['customer']['app_id'], self.customer.app_id)
        self.assertEqual(response.data['transaction']['marketplace']['name'], self.marketplace.name)

    def test_create_transaction_with_SKU_not_as_string(self):
        items = [{'ASIN': item.ASIN, 'count': 10} for item in self.items]
        request = self.factory.post('create_transaction', {'SKU': 1, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Company with provided SKU does not exist')

        request = self.factory.post('create_transaction', {'SKU': 0, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Company with provided SKU does not exist')

        request = self.factory.post('create_transaction', {'SKU': 0, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Company with provided SKU does not exist')

        request = self.factory.post('create_transaction', {'SKU': -1, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Company with provided SKU does not exist')

        request = self.factory.post('create_transaction', {'SKU': 1.1, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Company with provided SKU does not exist')

        request = self.factory.post('create_transaction', {'SKU': -1.1, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Company with provided SKU does not exist')

        request = self.factory.post('create_transaction', {'SKU': True, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Company with provided SKU does not exist')

        request = self.factory.post('create_transaction', {'SKU': False, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Company with provided SKU does not exist')

        request = self.factory.post('create_transaction', {'SKU': None, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Company with provided SKU does not exist')

        request = self.factory.post('create_transaction', {'SKU': list(), 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Company with provided SKU does not exist')

        request = self.factory.post('create_transaction', {'SKU': tuple(), 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Company with provided SKU does not exist')

        request = self.factory.post('create_transaction', {'SKU': dict(), 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Company with provided SKU does not exist')

        request = self.factory.post('create_transaction', {'SKU': set(), 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Company with provided SKU does not exist')

    def test_create_transaction_with_empty_SKU(self):
        items = [{'ASIN': item.ASIN, 'count': 10} for item in self.items]
        request = self.factory.post('create_transaction', {'SKU': '', 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Company with provided SKU does not exist')

        request = self.factory.post('create_transaction', {'SKU': ' ', 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Company with provided SKU does not exist')

    def test_create_transaction_with_too_long_SKU(self):
        items = [{'ASIN': item.ASIN, 'count': 10} for item in self.items]
        request = self.factory.post('create_transaction', {'SKU': '1 ' * 151, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Company with provided SKU does not exist')

    def test_create_transaction_with_app_id_not_as_string(self):
        items = [{'ASIN': item.ASIN, 'count': 10} for item in self.items]
        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': 1,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Customer with provided app_id does not exist')

        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': 0,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Customer with provided app_id does not exist')

        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': -1,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Customer with provided app_id does not exist')

        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': 1.1,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Customer with provided app_id does not exist')

        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': -1.1,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Customer with provided app_id does not exist')

        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': True,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Customer with provided app_id does not exist')

        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': False,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Customer with provided app_id does not exist')

        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': None,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Customer with provided app_id does not exist')

        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': list(),
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Customer with provided app_id does not exist')

        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': tuple(),
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Customer with provided app_id does not exist')

        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': dict(),
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Customer with provided app_id does not exist')

        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': set(),
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Customer with provided app_id does not exist')

    def test_create_transaction_with_empty_app_id(self):
        items = [{'ASIN': item.ASIN, 'count': 10} for item in self.items]
        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': '',
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Customer with provided app_id does not exist')

        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': ' ',
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Customer with provided app_id does not exist')

    def test_create_transaction_with_too_long_app_id(self):
        items = [{'ASIN': item.ASIN, 'count': 10} for item in self.items]
        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': '1' * 101,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Customer with provided app_id does not exist')

    def test_create_transaction_with_marketplace_name_not_as_string(self):
        items = [{'ASIN': item.ASIN, 'count': 10} for item in self.items]
        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': 1, 'country_code': 'PL', 'items': items},
                                    format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Marketplace with provided marketplace_name does not exist')

        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': 0, 'country_code': 'PL', 'items': items},
                                    format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Marketplace with provided marketplace_name does not exist')

        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': -1, 'country_code': 'PL',
                                                           'items': items}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Marketplace with provided marketplace_name does not exist')

        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': 1.1, 'country_code': 'PL',
                                                           'items': items}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Marketplace with provided marketplace_name does not exist')

        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': -1.1, 'country_code': 'PL',
                                                           'items': items}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Marketplace with provided marketplace_name does not exist')

        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': True, 'country_code': 'PL',
                                                           'items': items}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Marketplace with provided marketplace_name does not exist')

        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': False, 'country_code': 'PL',
                                                           'items': items}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Marketplace with provided marketplace_name does not exist')

        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': None, 'country_code': 'PL',
                                                           'items': items}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Marketplace with provided marketplace_name does not exist')

        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': list(), 'country_code': 'PL',
                                                           'items': items}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Marketplace with provided marketplace_name does not exist')

        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': tuple(), 'country_code': 'PL',
                                                           'items': items}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Marketplace with provided marketplace_name does not exist')

        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': dict(), 'country_code': 'PL',
                                                           'items': items}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Marketplace with provided marketplace_name does not exist')

        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': set(), 'country_code': 'PL',
                                                           'items': items}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Marketplace with provided marketplace_name does not exist')

    def test_create_transaction_with_empty_string_as_marketplace_name(self):
        items = [{'ASIN': item.ASIN, 'count': 10} for item in self.items]
        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': '', 'country_code': 'PL',
                                                           'items': items}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Marketplace with provided marketplace_name does not exist')

        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': ' ', 'country_code': 'PL',
                                                           'items': items}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Marketplace with provided marketplace_name does not exist')

    def test_create_transaction_with_too_long_string_as_marketplace_name(self):
        items = [{'ASIN': item.ASIN, 'count': 10} for item in self.items]
        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': '1' * 51, 'country_code': 'PL',
                                                           'items': items}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Marketplace with provided marketplace_name does not exist')

    def test_create_transaction_with_country_code_not_as_string(self):
        items = [{'ASIN': item.ASIN, 'count': 10} for item in self.items]
        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 1, 'items': items}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Country code error')

        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 0, 'items': items}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Country code error')

        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': -1, 'items': items}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Country code error')

        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 1.1, 'items': items}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Country code error')

        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': -1.1, 'items': items}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Country code error')

        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': True, 'items': items}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Country code error')

        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': False, 'items': items}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Country code error')

        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': None, 'items': items}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Country code error')

        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': list(), 'items': items}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Country code error')

        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': tuple(), 'items': items}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Country code error')

        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': dict(), 'items': items}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Country code error')

        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': set(), 'items': items}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Country code error')

    def test_create_transaction_with_items_not_as_iterable(self):
        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': ''}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'items should be list of dicts')

        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': ' '}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'items should be list of dicts')

        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': '1'}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'items should be list of dicts')

        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': '0'}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'items should be list of dicts')

        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': '-1'}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'items should be list of dicts')

        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': '1.1'}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'items should be list of dicts')

        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': '-1.1'}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'items should be list of dicts')

        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': 'Text'}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'items should be list of dicts')

        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': 1}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'items should be list of dicts')

        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': 0}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'items should be list of dicts')

        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': -1}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'items should be list of dicts')

        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': 1.1}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'items should be list of dicts')

        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': -1.1}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'items should be list of dicts')

        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': True}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'items should be list of dicts')

        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': False}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'items should be list of dicts')

        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': None}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'items should be list of dicts')

        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': dict()}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'items should be list of dicts')

        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': set()}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'items should be list of dicts')

    def test_create_transaction_with_tuple_as_items(self):
        items = ({'ASIN': item.ASIN, 'count': 10} for item in self.items)
        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 1)
        self.assertEqual(SoldItem.objects.count(), 4)
        self.assertEqual(response.data['status'], 'OK')
        self.assertEqual(response.data['transaction']['vendor']['SKU'], self.company.SKU)
        self.assertEqual(response.data['transaction']['customer']['app_id'], self.customer.app_id)
        self.assertEqual(response.data['transaction']['marketplace']['name'], self.marketplace.name)

    def test_create_transaction_with_not_dict_inside_items(self):
        items = ['' for _ in self.items]
        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'item should be dict')

        items = [' ' for _ in self.items]
        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'item should be dict')

        items = ['1' for _ in self.items]
        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'item should be dict')

        items = ['0' for _ in self.items]
        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'item should be dict')

        items = ['-1' for _ in self.items]
        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'item should be dict')

        items = ['1.1' for _ in self.items]
        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'item should be dict')

        items = ['-1.1' for _ in self.items]
        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'item should be dict')

        items = ['Text' for _ in self.items]
        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'item should be dict')

        items = [1 for _ in self.items]
        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'item should be dict')

        items = [0 for _ in self.items]
        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'item should be dict')

        items = [-1 for _ in self.items]
        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'item should be dict')

        items = [1.1 for _ in self.items]
        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'item should be dict')

        items = [-1.1 for _ in self.items]
        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'item should be dict')

        items = [True for _ in self.items]
        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'item should be dict')

        items = [False for _ in self.items]
        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'item should be dict')

        items = [None for _ in self.items]
        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'item should be dict')

        items = [list() for _ in self.items]
        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'item should be dict')

        items = [tuple() for _ in self.items]
        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'item should be dict')

        items = [set() for _ in self.items]
        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'item should be dict')

    def test_create_transaction_with_not_expected_keys_in_item(self):
        items = [dict() for _ in self.items]
        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'each item should contain \'ASIN\' and \'count\' keys')

    def test_create_transaction_with_not_string_as_ASIN(self):
        items = [{'ASIN': 1, 'count': 10}]
        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'sequence item 0: expected str instance, int found')

        items = [{'ASIN': 0, 'count': 10}]
        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'sequence item 0: expected str instance, int found')

        items = [{'ASIN': -1, 'count': 10}]
        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'sequence item 0: expected str instance, int found')

        items = [{'ASIN': 1.1, 'count': 10}]
        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'sequence item 0: expected str instance, float found')

        items = [{'ASIN': -1.1, 'count': 10}]
        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'sequence item 0: expected str instance, float found')

        items = [{'ASIN': True, 'count': 10}]
        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'sequence item 0: expected str instance, bool found')

        items = [{'ASIN': False, 'count': 10}]
        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'sequence item 0: expected str instance, bool found')

        items = [{'ASIN': None, 'count': 10}]
        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'sequence item 0: expected str instance, NoneType found')

        items = [{'ASIN': list(), 'count': 10}]
        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'sequence item 0: expected str instance, list found')

        items = [{'ASIN': tuple(), 'count': 10}]
        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'sequence item 0: expected str instance, list found')

        items = [{'ASIN': dict(), 'count': 10}]
        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'sequence item 0: expected str instance, dict found')

        items = [{'ASIN': set(), 'count': 10}]
        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'sequence item 0: expected str instance, list found')

    def test_create_transaction_with_not_existing_ASIN(self):
        items = [{'ASIN': '1', 'count': 10}]
        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'items error: 1')

    def test_create_transaction_with_empty_string_as_ASIN(self):
        items = [{'ASIN': '', 'count': 10}]
        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'items error: ')

        items = [{'ASIN': ' ', 'count': 10}]
        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'items error:  ')

    def test_create_transaction_without_ASIN(self):
        items = [{'count': 10}]
        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'each item should contain \'ASIN\' and \'count\' keys')

    def test_create_transaction_with_not_int_as_count(self):
        items = [{'ASIN': item.ASIN, 'count': ''} for item in self.items]
        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'items error: {}, {}, {}, {}'.format(
            self.items[0].ASIN, self.items[1].ASIN, self.items[2].ASIN, self.items[3].ASIN))

        items = [{'ASIN': item.ASIN, 'count': ' '} for item in self.items]
        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'items error: {}, {}, {}, {}'.format(
            self.items[0].ASIN, self.items[1].ASIN, self.items[2].ASIN, self.items[3].ASIN))

        items = [{'ASIN': item.ASIN, 'count': '1'} for item in self.items]
        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'items error: {}, {}, {}, {}'.format(
            self.items[0].ASIN, self.items[1].ASIN, self.items[2].ASIN, self.items[3].ASIN))

        items = [{'ASIN': item.ASIN, 'count': '0'} for item in self.items]
        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'items error: {}, {}, {}, {}'.format(
            self.items[0].ASIN, self.items[1].ASIN, self.items[2].ASIN, self.items[3].ASIN))

        items = [{'ASIN': item.ASIN, 'count': '-1'} for item in self.items]
        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'items error: {}, {}, {}, {}'.format(
            self.items[0].ASIN, self.items[1].ASIN, self.items[2].ASIN, self.items[3].ASIN))

        items = [{'ASIN': item.ASIN, 'count': '1.1'} for item in self.items]
        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'items error: {}, {}, {}, {}'.format(
            self.items[0].ASIN, self.items[1].ASIN, self.items[2].ASIN, self.items[3].ASIN))

        items = [{'ASIN': item.ASIN, 'count': '-1.1'} for item in self.items]
        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'items error: {}, {}, {}, {}'.format(
            self.items[0].ASIN, self.items[1].ASIN, self.items[2].ASIN, self.items[3].ASIN))

        items = [{'ASIN': item.ASIN, 'count': 'Text'} for item in self.items]
        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'items error: {}, {}, {}, {}'.format(
            self.items[0].ASIN, self.items[1].ASIN, self.items[2].ASIN, self.items[3].ASIN))

        items = [{'ASIN': item.ASIN, 'count': 1.1} for item in self.items]
        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'items error: {}, {}, {}, {}'.format(
            self.items[0].ASIN, self.items[1].ASIN, self.items[2].ASIN, self.items[3].ASIN))

        items = [{'ASIN': item.ASIN, 'count': -1.1} for item in self.items]
        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'items error: {}, {}, {}, {}'.format(
            self.items[0].ASIN, self.items[1].ASIN, self.items[2].ASIN, self.items[3].ASIN))

        items = [{'ASIN': item.ASIN, 'count': True} for item in self.items]
        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'items error: {}, {}, {}, {}'.format(
            self.items[0].ASIN, self.items[1].ASIN, self.items[2].ASIN, self.items[3].ASIN))

        items = [{'ASIN': item.ASIN, 'count': False} for item in self.items]
        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'items error: {}, {}, {}, {}'.format(
            self.items[0].ASIN, self.items[1].ASIN, self.items[2].ASIN, self.items[3].ASIN))

        items = [{'ASIN': item.ASIN, 'count': None} for item in self.items]
        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'items error: {}, {}, {}, {}'.format(
            self.items[0].ASIN, self.items[1].ASIN, self.items[2].ASIN, self.items[3].ASIN))

        items = [{'ASIN': item.ASIN, 'count': list()} for item in self.items]
        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'items error: {}, {}, {}, {}'.format(
            self.items[0].ASIN, self.items[1].ASIN, self.items[2].ASIN, self.items[3].ASIN))

        items = [{'ASIN': item.ASIN, 'count': tuple()} for item in self.items]
        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'items error: {}, {}, {}, {}'.format(
            self.items[0].ASIN, self.items[1].ASIN, self.items[2].ASIN, self.items[3].ASIN))

        items = [{'ASIN': item.ASIN, 'count': dict()} for item in self.items]
        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'items error: {}, {}, {}, {}'.format(
            self.items[0].ASIN, self.items[1].ASIN, self.items[2].ASIN, self.items[3].ASIN))

        items = [{'ASIN': item.ASIN, 'count': set()} for item in self.items]
        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'items error: {}, {}, {}, {}'.format(
            self.items[0].ASIN, self.items[1].ASIN, self.items[2].ASIN, self.items[3].ASIN))

    def test_create_transaction_without_count(self):
        items = [{'ASIN': item.ASIN} for item in self.items]
        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'each item should contain \'ASIN\' and \'count\' keys')

    def test_create_transaction_without_arguments(self):
        items = [{'ASIN': item.ASIN, 'count': 10} for item in self.items]
        request = self.factory.post('create_transaction', {'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'missing argument: SKU')

        request = self.factory.post('create_transaction', {'SKU': self.company.SKU,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'missing argument: app_id')

        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'country_code': 'PL', 'items': items}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'missing argument: marketplace_name')

        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name, 'items': items},
                                    format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'missing 1 required positional argument: \'country_code\'')

        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL'}, format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'missing argument: items')

    def test_create_transaction_with_refund(self):
        items = [{'ASIN': item.ASIN, 'count': 10} for item in self.items]
        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items, 'refund': True},
                                    format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 1)
        self.assertEqual(SoldItem.objects.count(), 4)
        self.assertEqual(response.data['status'], 'OK')
        self.assertEqual(response.data['transaction']['vendor']['SKU'], self.company.SKU)
        self.assertEqual(response.data['transaction']['customer']['app_id'], self.customer.app_id)
        self.assertEqual(response.data['transaction']['marketplace']['name'], self.marketplace.name)
        self.assertTrue(response.data['transaction']['refund'])

        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items, 'refund': False},
                                    format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 2)
        self.assertEqual(SoldItem.objects.count(), 8)
        self.assertEqual(response.data['status'], 'OK')
        self.assertEqual(response.data['transaction']['vendor']['SKU'], self.company.SKU)
        self.assertEqual(response.data['transaction']['customer']['app_id'], self.customer.app_id)
        self.assertEqual(response.data['transaction']['marketplace']['name'], self.marketplace.name)
        self.assertFalse(response.data['transaction']['refund'])

    def test_create_transaction_with_not_bool_as_refund(self):
        items = [{'ASIN': item.ASIN, 'count': 10} for item in self.items]
        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items, 'refund': ''},
                                    format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Refund error')

        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items, 'refund': ' '},
                                    format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Refund error')

        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items, 'refund': '1'},
                                    format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Refund error')

        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items, 'refund': '0'},
                                    format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Refund error')

        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items, 'refund': '-1'},
                                    format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Refund error')

        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items, 'refund': '1.1'},
                                    format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Refund error')

        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items, 'refund': '-1.1'},
                                    format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Refund error')

        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items, 'refund': 'Text'},
                                    format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Refund error')

        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items, 'refund': 1},
                                    format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Refund error')

        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items, 'refund': 0},
                                    format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Refund error')

        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items, 'refund': -1},
                                    format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Refund error')

        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items, 'refund': 1.1},
                                    format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Refund error')

        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items, 'refund': -1.1},
                                    format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Refund error')

        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items, 'refund': None},
                                    format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Refund error')

        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items, 'refund': list()},
                                    format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Refund error')

        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items, 'refund': tuple()},
                                    format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Refund error')

        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items, 'refund': dict()},
                                    format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Refund error')

        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items, 'refund': set()},
                                    format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Refund error')

    def test_create_transaction_with_adjustment(self):
        items = [{'ASIN': item.ASIN, 'count': 10} for item in self.items]
        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items, 'adjustment': True},
                                    format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 1)
        self.assertEqual(SoldItem.objects.count(), 4)
        self.assertEqual(response.data['status'], 'OK')
        self.assertEqual(response.data['transaction']['vendor']['SKU'], self.company.SKU)
        self.assertEqual(response.data['transaction']['customer']['app_id'], self.customer.app_id)
        self.assertEqual(response.data['transaction']['marketplace']['name'], self.marketplace.name)
        self.assertTrue(response.data['transaction']['adjustment'])

        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items, 'adjustment': False},
                                    format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 2)
        self.assertEqual(SoldItem.objects.count(), 8)
        self.assertEqual(response.data['status'], 'OK')
        self.assertEqual(response.data['transaction']['vendor']['SKU'], self.company.SKU)
        self.assertEqual(response.data['transaction']['customer']['app_id'], self.customer.app_id)
        self.assertEqual(response.data['transaction']['marketplace']['name'], self.marketplace.name)
        self.assertFalse(response.data['transaction']['adjustment'])

    def test_create_transaction_with_not_bool_as_adjustment(self):
        items = [{'ASIN': item.ASIN, 'count': 10} for item in self.items]
        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items, 'adjustment': ''},
                                    format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Adjustment error')

        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items, 'adjustment': '1'},
                                    format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Adjustment error')

        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items, 'adjustment': '0'},
                                    format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Adjustment error')

        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items, 'adjustment': '-1'},
                                    format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Adjustment error')

        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items, 'adjustment': '1.1'},
                                    format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Adjustment error')

        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items, 'adjustment': '-1.1'},
                                    format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Adjustment error')

        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items, 'adjustment': 'Text'},
                                    format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Adjustment error')

        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items, 'adjustment': 1},
                                    format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Adjustment error')

        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items, 'adjustment': 0},
                                    format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Adjustment error')

        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items, 'adjustment': -1},
                                    format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Adjustment error')

        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items, 'adjustment': 1.1},
                                    format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Adjustment error')

        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items, 'adjustment': -1.1},
                                    format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Adjustment error')

        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items, 'adjustment': None},
                                    format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Adjustment error')

        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items, 'adjustment': list()},
                                    format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Adjustment error')

        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items, 'adjustment': tuple()},
                                    format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Adjustment error')

        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items, 'adjustment': dict()},
                                    format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Adjustment error')

        request = self.factory.post('create_transaction', {'SKU': self.company.SKU, 'app_id': self.customer.app_id,
                                                           'marketplace_name': self.marketplace.name,
                                                           'country_code': 'PL', 'items': items, 'adjustment': set()},
                                    format='json')
        response = self.view(request)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(SoldItem.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Adjustment error')
