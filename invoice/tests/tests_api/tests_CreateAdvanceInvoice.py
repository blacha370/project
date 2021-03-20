from rest_framework.test import APITestCase, APIRequestFactory
from django.contrib.auth.models import User
from ...views import (CreateAdvanceInvoice, AdvanceInvoice, Invoice, Receipt, Transaction, Company, Customer, Marketplace,
                      SoldItem, Item, Tax, Address)


class CreateAdvanceInvoiceTestCase(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = CreateAdvanceInvoice.as_view()
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
        self.receipt = Receipt.create(transaction=self.transaction)
        self.invoice = Invoice.create(receipt=self.receipt)

    def test_create_advance_invoice(self):
        request = self.factory.post('create_advance_invoice', {'invoice_id': self.invoice.invoice_id,
                                                               'payment': 100.02}, format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(AdvanceInvoice.objects.count(), 1)
        self.assertEqual(response.data['status'], 'OK')
        self.assertEqual(response.data['advance_invoice']['advance_invoice_id'], self.invoice.invoice_id + '-01')

    def test_create_invoice_until_ended(self):
        request = self.factory.post('create_advance_invoice', {'invoice_id': self.invoice.invoice_id,
                                                               'payment': 100.02}, format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(AdvanceInvoice.objects.count(), 1)
        self.assertEqual(response.data['status'], 'OK')
        self.assertEqual(response.data['advance_invoice']['advance_invoice_id'], self.invoice.invoice_id + '-01')

        request = self.factory.post('create_advance_invoice', {'invoice_id': self.invoice.invoice_id,
                                                               'payment': 438}, format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(AdvanceInvoice.objects.count(), 2)
        self.assertEqual(response.data['status'], 'OK')
        self.assertEqual(response.data['advance_invoice']['advance_invoice_id'], self.invoice.invoice_id + '-02')
        self.assertTrue(Invoice.objects.get(pk=1).ended)

    def test_create_invoice_with_value_above_transaction_total_value(self):
        request = self.factory.post('create_advance_invoice', {'invoice_id': self.invoice.invoice_id,
                                                               'payment': 1000}, format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(AdvanceInvoice.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Value error')
        self.assertFalse(Invoice.objects.get(pk=1).ended)

    def test_create_advance_invoice_with_not_string_as_invoice_id(self):
        request = self.factory.post('create_advance_invoice', {'invoice_id': 1, 'payment': 1000}, format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(AdvanceInvoice.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Invoice with provided invoice_id does not exist')

        request = self.factory.post('create_advance_invoice', {'invoice_id': 0, 'payment': 1000}, format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(AdvanceInvoice.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Invoice with provided invoice_id does not exist')

        request = self.factory.post('create_advance_invoice', {'invoice_id': -1, 'payment': 1000}, format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(AdvanceInvoice.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Invoice with provided invoice_id does not exist')

        request = self.factory.post('create_advance_invoice', {'invoice_id': 1.1, 'payment': 1000}, format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(AdvanceInvoice.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Invoice with provided invoice_id does not exist')

        request = self.factory.post('create_advance_invoice', {'invoice_id': -1.1, 'payment': 1000}, format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(AdvanceInvoice.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Invoice with provided invoice_id does not exist')

        request = self.factory.post('create_advance_invoice', {'invoice_id': True, 'payment': 1000}, format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(AdvanceInvoice.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Invoice with provided invoice_id does not exist')

        request = self.factory.post('create_advance_invoice', {'invoice_id': False, 'payment': 1000}, format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(AdvanceInvoice.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Invoice with provided invoice_id does not exist')

        request = self.factory.post('create_advance_invoice', {'invoice_id': None, 'payment': 1000}, format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(AdvanceInvoice.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Invoice with provided invoice_id does not exist')

        request = self.factory.post('create_advance_invoice', {'invoice_id': list(), 'payment': 1000}, format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(AdvanceInvoice.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Invoice with provided invoice_id does not exist')

        request = self.factory.post('create_advance_invoice', {'invoice_id': tuple(), 'payment': 1000}, format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(AdvanceInvoice.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Invoice with provided invoice_id does not exist')

        request = self.factory.post('create_advance_invoice', {'invoice_id': dict(), 'payment': 1000}, format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(AdvanceInvoice.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Invoice with provided invoice_id does not exist')

        request = self.factory.post('create_advance_invoice', {'invoice_id': set(), 'payment': 1000}, format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(AdvanceInvoice.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Invoice with provided invoice_id does not exist')

    def test_create_advance_invoice_with_empty_string_as_invoice_id(self):
        request = self.factory.post('create_advance_invoice', {'invoice_id': '', 'payment': 1000}, format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(AdvanceInvoice.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Invoice with provided invoice_id does not exist')

        request = self.factory.post('create_advance_invoice', {'invoice_id': ' ', 'payment': 1000}, format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(AdvanceInvoice.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Invoice with provided invoice_id does not exist')

    def test_create_advance_invoice_with_wrong_invoice_id(self):
        request = self.factory.post('create_advance_invoice', {'invoice_id': 'wrong_id', 'payment': 1000},
                                    format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(AdvanceInvoice.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Invoice with provided invoice_id does not exist')

    def test_crate_advance_invoice_without_invoice_id(self):
        request = self.factory.post('create_advance_invoice', {'payment': 1000}, format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(AdvanceInvoice.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'missing argument: \'invoice_id\'')

    def test_create_advance_invoice_with_not_int_or_float_as_payment(self):
        request = self.factory.post('create_advance_invoice', {'invoice_id': self.invoice.invoice_id, 'payment': ''},
                                    format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(AdvanceInvoice.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Payment error')

        request = self.factory.post('create_advance_invoice', {'invoice_id': self.invoice.invoice_id, 'payment': ' '},
                                    format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(AdvanceInvoice.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Payment error')

        request = self.factory.post('create_advance_invoice', {'invoice_id': self.invoice.invoice_id, 'payment': '1'},
                                    format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(AdvanceInvoice.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Payment error')

        request = self.factory.post('create_advance_invoice', {'invoice_id': self.invoice.invoice_id, 'payment': '0'},
                                    format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(AdvanceInvoice.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Payment error')

        request = self.factory.post('create_advance_invoice', {'invoice_id': self.invoice.invoice_id, 'payment': '-1'},
                                    format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(AdvanceInvoice.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Payment error')

        request = self.factory.post('create_advance_invoice', {'invoice_id': self.invoice.invoice_id, 'payment': '1.1'},
                                    format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(AdvanceInvoice.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Payment error')

        request = self.factory.post('create_advance_invoice', {'invoice_id': self.invoice.invoice_id,
                                                               'payment': '-1.1'}, format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(AdvanceInvoice.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Payment error')

        request = self.factory.post('create_advance_invoice', {'invoice_id': self.invoice.invoice_id,
                                                               'payment': 'Text'}, format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(AdvanceInvoice.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Payment error')

        request = self.factory.post('create_advance_invoice', {'invoice_id': self.invoice.invoice_id, 'payment': 0},
                                    format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(AdvanceInvoice.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Payment error')

        request = self.factory.post('create_advance_invoice', {'invoice_id': self.invoice.invoice_id, 'payment': True},
                                    format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(AdvanceInvoice.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Payment error')

        request = self.factory.post('create_advance_invoice', {'invoice_id': self.invoice.invoice_id, 'payment': False},
                                    format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(AdvanceInvoice.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Payment error')

        request = self.factory.post('create_advance_invoice', {'invoice_id': self.invoice.invoice_id, 'payment': None},
                                    format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(AdvanceInvoice.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Payment error')

        request = self.factory.post('create_advance_invoice', {'invoice_id': self.invoice.invoice_id,
                                                               'payment': list()}, format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(AdvanceInvoice.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Payment error')

        request = self.factory.post('create_advance_invoice', {'invoice_id': self.invoice.invoice_id,
                                                               'payment': tuple()}, format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(AdvanceInvoice.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Payment error')

        request = self.factory.post('create_advance_invoice', {'invoice_id': self.invoice.invoice_id,
                                                               'payment': dict()}, format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(AdvanceInvoice.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Payment error')

        request = self.factory.post('create_advance_invoice', {'invoice_id': self.invoice.invoice_id, 'payment': set()},
                                    format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(AdvanceInvoice.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Payment error')

    def test_create_advance_invoice_with_negative_or_0_as_payment(self):
        request = self.factory.post('create_advance_invoice', {'invoice_id': self.invoice.invoice_id, 'payment': 0},
                                    format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(AdvanceInvoice.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Payment error')

        request = self.factory.post('create_advance_invoice', {'invoice_id': self.invoice.invoice_id, 'payment': -1},
                                    format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(AdvanceInvoice.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Payment error')

        request = self.factory.post('create_advance_invoice', {'invoice_id': self.invoice.invoice_id, 'payment': -1.1},
                                    format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(AdvanceInvoice.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Payment error')
