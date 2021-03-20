from rest_framework.test import APITestCase, APIRequestFactory
from django.contrib.auth.models import User
from ...views import CreateReceipt, Receipt, Transaction, Company, Customer, Marketplace, SoldItem, Item, Tax, Address


class CreateReceiptTestCase(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = CreateReceipt.as_view()
        self.user = User(username='test', password='test')
        self.user.save()
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
        self.transaction = Transaction.create(vendor=self.company, customer=self.customer, marketplace=self.marketplace,
                                              country_code='PL')
        for item in Item.objects.all():
            self.transaction.items.add(SoldItem.create(item=item, units=10))

    def test_create_receipt(self):
        request = self.factory.post('crate_receipt', {'transaction_id': self.transaction.transaction_id}, format='json')
        request.user = self.user
        response = self.view(request)
        receipt = Receipt.objects.get(pk=1)
        self.assertEqual(Receipt.objects.count(), 1)
        self.assertEqual(response.data['status'], 'OK')
        self.assertEqual(response.data['receipt']['receipt_id'], receipt.receipt_id)
        self.assertEqual(response.data['receipt']['transaction']['transaction_id'], self.transaction.transaction_id)

    def test_create_second_invoice_with_same_transaction_id(self):
        request = self.factory.post('crate_receipt', {'transaction_id': self.transaction.transaction_id}, format='json')
        request.user = self.user
        response = self.view(request)
        receipt = Receipt.objects.get(pk=1)
        self.assertEqual(Receipt.objects.count(), 1)
        self.assertEqual(response.data['status'], 'OK')
        self.assertEqual(response.data['receipt']['receipt_id'], receipt.receipt_id)
        self.assertEqual(response.data['receipt']['transaction']['transaction_id'], self.transaction.transaction_id)

        request = self.factory.post('crate_receipt', {'transaction_id': self.transaction.transaction_id}, format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(Receipt.objects.count(), 1)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Transaction error')

    def test_create_receipt_with_not_valid_transaction_id(self):
        request = self.factory.post('crate_receipt', {'transaction_id': 'not_valid_transaction_id'}, format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(Receipt.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Transaction with provided id does not exist')

    def test_create_receipt_with_not_string_as_transaction_id(self):
        request = self.factory.post('crate_receipt', {'transaction_id': 1}, format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(Receipt.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Transaction with provided id does not exist')

        request = self.factory.post('crate_receipt', {'transaction_id': 0}, format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(Receipt.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Transaction with provided id does not exist')

        request = self.factory.post('crate_receipt', {'transaction_id': -1}, format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(Receipt.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Transaction with provided id does not exist')

        request = self.factory.post('crate_receipt', {'transaction_id': 1.1}, format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(Receipt.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Transaction with provided id does not exist')

        request = self.factory.post('crate_receipt', {'transaction_id': -1.1}, format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(Receipt.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Transaction with provided id does not exist')

        request = self.factory.post('crate_receipt', {'transaction_id': True}, format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(Receipt.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Transaction with provided id does not exist')

        request = self.factory.post('crate_receipt', {'transaction_id': False}, format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(Receipt.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Transaction with provided id does not exist')

        request = self.factory.post('crate_receipt', {'transaction_id': None}, format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(Receipt.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Transaction with provided id does not exist')

        request = self.factory.post('crate_receipt', {'transaction_id': list()}, format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(Receipt.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Transaction with provided id does not exist')

        request = self.factory.post('crate_receipt', {'transaction_id': tuple()}, format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(Receipt.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Transaction with provided id does not exist')

        request = self.factory.post('crate_receipt', {'transaction_id': dict()}, format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(Receipt.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Transaction with provided id does not exist')

        request = self.factory.post('crate_receipt', {'transaction_id': set()}, format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(Receipt.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Transaction with provided id does not exist')

    def test_create_receipt_without_transaction_id(self):
        request = self.factory.post('crate_receipt', {}, format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(Receipt.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'missing argument: transaction_id')

    def test_create_receipt_with_empty_string_as_transaction_id(self):
        request = self.factory.post('crate_receipt', {'transaction_id': ''}, format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(Receipt.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Transaction with provided id does not exist')

        request = self.factory.post('crate_receipt', {'transaction_id': ' '}, format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(Receipt.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Transaction with provided id does not exist')

    def test_create_receipt_with_no_post_data(self):
        request = self.factory.post('crate_receipt', format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(Receipt.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'missing argument: transaction_id')
