from rest_framework.test import APITestCase, APIRequestFactory
from ...views import (CreateInvoice, Invoice, Receipt, Transaction, Company, Customer, Marketplace, SoldItem, Item, Tax,
                      Address)


class CreateInvoiceTestCase(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = CreateInvoice.as_view()
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

    def test_create_invoice(self):
        request = self.factory.post('create_invoice', {'receipt_id': self.receipt.receipt_id}, format='json')
        response = self.view(request)
        invoice = Invoice.objects.get(pk=1)
        self.assertEqual(Invoice.objects.count(), 1)
        self.assertEqual(response.data['status'], 'OK')
        self.assertEqual(response.data['invoice']['invoice_id'], invoice.invoice_id)
        self.assertEqual(response.data['invoice']['receipt']['receipt_id'], self.receipt.receipt_id)
        self.assertEqual(response.data['invoice']['receipt']['transaction']['transaction_id'],
                         self.transaction.transaction_id)
        self.assertFalse(response.data['invoice']['ended'])

    def test_create_second_invoice_with_same_number(self):
        request = self.factory.post('create_invoice', {'receipt_id': self.receipt.receipt_id}, format='json')
        response = self.view(request)
        invoice = Invoice.objects.get(pk=1)
        self.assertEqual(Invoice.objects.count(), 1)
        self.assertEqual(response.data['status'], 'OK')
        self.assertEqual(response.data['invoice']['invoice_id'], invoice.invoice_id)
        self.assertEqual(response.data['invoice']['receipt']['receipt_id'], self.receipt.receipt_id)
        self.assertEqual(response.data['invoice']['receipt']['transaction']['transaction_id'],
                         self.transaction.transaction_id)
        self.assertFalse(response.data['invoice']['ended'])

        request = self.factory.post('create_invoice', {'receipt_id': self.receipt.receipt_id}, format='json')
        response = self.view(request)
        self.assertEqual(Invoice.objects.count(), 1)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Receipt error')

    def test_create_invoice_with_ended_parameter(self):
        request = self.factory.post('create_invoice', {'receipt_id': self.receipt.receipt_id, 'ended': True},
                                    format='json')
        response = self.view(request)
        invoice = Invoice.objects.get(pk=1)
        self.assertEqual(Invoice.objects.count(), 1)
        self.assertEqual(response.data['status'], 'OK')
        self.assertEqual(response.data['invoice']['invoice_id'], invoice.invoice_id)
        self.assertEqual(response.data['invoice']['receipt']['receipt_id'], self.receipt.receipt_id)
        self.assertEqual(response.data['invoice']['receipt']['transaction']['transaction_id'],
                         self.transaction.transaction_id)
        self.assertTrue(response.data['invoice']['ended'])

        invoice.delete()
        request = self.factory.post('create_invoice', {'receipt_id': self.receipt.receipt_id, 'ended': False},
                                    format='json')
        response = self.view(request)
        invoice = Invoice.objects.get(pk=2)
        self.assertEqual(Invoice.objects.count(), 1)
        self.assertEqual(response.data['status'], 'OK')
        self.assertEqual(response.data['invoice']['invoice_id'], invoice.invoice_id)
        self.assertEqual(response.data['invoice']['receipt']['receipt_id'], self.receipt.receipt_id)
        self.assertEqual(response.data['invoice']['receipt']['transaction']['transaction_id'],
                         self.transaction.transaction_id)
        self.assertFalse(response.data['invoice']['ended'])

    def test_create_invoice_with_not_string_as_receipt_it(self):
        request = self.factory.post('create_invoice', {'receipt_id': 1}, format='json')
        response = self.view(request)
        self.assertEqual(Invoice.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Receipt with provided receipt_id does not exist')

        request = self.factory.post('create_invoice', {'receipt_id': 0}, format='json')
        response = self.view(request)
        self.assertEqual(Invoice.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Receipt with provided receipt_id does not exist')

        request = self.factory.post('create_invoice', {'receipt_id': -1}, format='json')
        response = self.view(request)
        self.assertEqual(Invoice.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Receipt with provided receipt_id does not exist')

        request = self.factory.post('create_invoice', {'receipt_id': 1.1}, format='json')
        response = self.view(request)
        self.assertEqual(Invoice.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Receipt with provided receipt_id does not exist')

        request = self.factory.post('create_invoice', {'receipt_id': -1.1}, format='json')
        response = self.view(request)
        self.assertEqual(Invoice.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Receipt with provided receipt_id does not exist')

        request = self.factory.post('create_invoice', {'receipt_id': None}, format='json')
        response = self.view(request)
        self.assertEqual(Invoice.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Receipt with provided receipt_id does not exist')

        request = self.factory.post('create_invoice', {'receipt_id': list()}, format='json')
        response = self.view(request)
        self.assertEqual(Invoice.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Receipt with provided receipt_id does not exist')

        request = self.factory.post('create_invoice', {'receipt_id': tuple()}, format='json')
        response = self.view(request)
        self.assertEqual(Invoice.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Receipt with provided receipt_id does not exist')

        request = self.factory.post('create_invoice', {'receipt_id': dict()}, format='json')
        response = self.view(request)
        self.assertEqual(Invoice.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Receipt with provided receipt_id does not exist')

        request = self.factory.post('create_invoice', {'receipt_id': set()}, format='json')
        response = self.view(request)
        self.assertEqual(Invoice.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Receipt with provided receipt_id does not exist')

    def test_create_invoice_with_empty_string_as_receipt_id(self):
        request = self.factory.post('create_invoice', {'receipt_id': ''}, format='json')
        response = self.view(request)
        self.assertEqual(Invoice.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Receipt with provided receipt_id does not exist')

        request = self.factory.post('create_invoice', {'receipt_id': ' '}, format='json')
        response = self.view(request)
        self.assertEqual(Invoice.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Receipt with provided receipt_id does not exist')

    def test_create_invoice_with_too_long_string_as_receipt_id(self):
        request = self.factory.post('create_invoice', {'receipt_id': '1' * 21}, format='json')
        response = self.view(request)
        self.assertEqual(Invoice.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Receipt with provided receipt_id does not exist')

    def test_create_invoice_without_receipt_id_argument(self):
        request = self.factory.post('create_invoice', {}, format='json')
        response = self.view(request)
        self.assertEqual(Invoice.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'missing argument: receipt_id')

    def test_create_invoice_with_not_bool_as_ended(self):
        request = self.factory.post('create_invoice', {'receipt_id': self.receipt.receipt_id, 'ended': ''},
                                    format='json')
        response = self.view(request)
        invoice = Invoice.objects.get(pk=1)
        self.assertEqual(Invoice.objects.count(), 1)
        self.assertEqual(response.data['status'], 'OK')
        self.assertEqual(response.data['invoice']['invoice_id'], invoice.invoice_id)
        self.assertEqual(response.data['invoice']['receipt']['receipt_id'], self.receipt.receipt_id)
        self.assertEqual(response.data['invoice']['receipt']['transaction']['transaction_id'],
                         self.transaction.transaction_id)
        self.assertFalse(response.data['invoice']['ended'])

        invoice.delete()
        request = self.factory.post('create_invoice', {'receipt_id': self.receipt.receipt_id, 'ended': ' '},
                                    format='json')
        response = self.view(request)
        invoice = Invoice.objects.get(pk=2)
        self.assertEqual(Invoice.objects.count(), 1)
        self.assertEqual(response.data['status'], 'OK')
        self.assertEqual(response.data['invoice']['invoice_id'], invoice.invoice_id)
        self.assertEqual(response.data['invoice']['receipt']['receipt_id'], self.receipt.receipt_id)
        self.assertEqual(response.data['invoice']['receipt']['transaction']['transaction_id'],
                         self.transaction.transaction_id)
        self.assertFalse(response.data['invoice']['ended'])

        invoice.delete()
        request = self.factory.post('create_invoice', {'receipt_id': self.receipt.receipt_id, 'ended': '1'},
                                    format='json')
        response = self.view(request)
        invoice = Invoice.objects.get(pk=3)
        self.assertEqual(Invoice.objects.count(), 1)
        self.assertEqual(response.data['status'], 'OK')
        self.assertEqual(response.data['invoice']['invoice_id'], invoice.invoice_id)
        self.assertEqual(response.data['invoice']['receipt']['receipt_id'], self.receipt.receipt_id)
        self.assertEqual(response.data['invoice']['receipt']['transaction']['transaction_id'],
                         self.transaction.transaction_id)
        self.assertFalse(response.data['invoice']['ended'])

        invoice.delete()
        request = self.factory.post('create_invoice', {'receipt_id': self.receipt.receipt_id, 'ended': '0'},
                                    format='json')
        response = self.view(request)
        invoice = Invoice.objects.get(pk=4)
        self.assertEqual(Invoice.objects.count(), 1)
        self.assertEqual(response.data['status'], 'OK')
        self.assertEqual(response.data['invoice']['invoice_id'], invoice.invoice_id)
        self.assertEqual(response.data['invoice']['receipt']['receipt_id'], self.receipt.receipt_id)
        self.assertEqual(response.data['invoice']['receipt']['transaction']['transaction_id'],
                         self.transaction.transaction_id)
        self.assertFalse(response.data['invoice']['ended'])

        invoice.delete()
        request = self.factory.post('create_invoice', {'receipt_id': self.receipt.receipt_id, 'ended': '-1'},
                                    format='json')
        response = self.view(request)
        invoice = Invoice.objects.get(pk=5)
        self.assertEqual(Invoice.objects.count(), 1)
        self.assertEqual(response.data['status'], 'OK')
        self.assertEqual(response.data['invoice']['invoice_id'], invoice.invoice_id)
        self.assertEqual(response.data['invoice']['receipt']['receipt_id'], self.receipt.receipt_id)
        self.assertEqual(response.data['invoice']['receipt']['transaction']['transaction_id'],
                         self.transaction.transaction_id)
        self.assertFalse(response.data['invoice']['ended'])

        invoice.delete()
        request = self.factory.post('create_invoice', {'receipt_id': self.receipt.receipt_id, 'ended': '1.1'},
                                    format='json')
        response = self.view(request)
        invoice = Invoice.objects.get(pk=6)
        self.assertEqual(Invoice.objects.count(), 1)
        self.assertEqual(response.data['status'], 'OK')
        self.assertEqual(response.data['invoice']['invoice_id'], invoice.invoice_id)
        self.assertEqual(response.data['invoice']['receipt']['receipt_id'], self.receipt.receipt_id)
        self.assertEqual(response.data['invoice']['receipt']['transaction']['transaction_id'],
                         self.transaction.transaction_id)
        self.assertFalse(response.data['invoice']['ended'])

        invoice.delete()
        request = self.factory.post('create_invoice', {'receipt_id': self.receipt.receipt_id, 'ended': '-1.1'},
                                    format='json')
        response = self.view(request)
        invoice = Invoice.objects.get(pk=7)
        self.assertEqual(Invoice.objects.count(), 1)
        self.assertEqual(response.data['status'], 'OK')
        self.assertEqual(response.data['invoice']['invoice_id'], invoice.invoice_id)
        self.assertEqual(response.data['invoice']['receipt']['receipt_id'], self.receipt.receipt_id)
        self.assertEqual(response.data['invoice']['receipt']['transaction']['transaction_id'],
                         self.transaction.transaction_id)
        self.assertFalse(response.data['invoice']['ended'])

        invoice.delete()
        request = self.factory.post('create_invoice', {'receipt_id': self.receipt.receipt_id, 'ended': 'Text'},
                                    format='json')
        response = self.view(request)
        invoice = Invoice.objects.get(pk=8)
        self.assertEqual(Invoice.objects.count(), 1)
        self.assertEqual(response.data['status'], 'OK')
        self.assertEqual(response.data['invoice']['invoice_id'], invoice.invoice_id)
        self.assertEqual(response.data['invoice']['receipt']['receipt_id'], self.receipt.receipt_id)
        self.assertEqual(response.data['invoice']['receipt']['transaction']['transaction_id'],
                         self.transaction.transaction_id)
        self.assertFalse(response.data['invoice']['ended'])

        invoice.delete()
        request = self.factory.post('create_invoice', {'receipt_id': self.receipt.receipt_id, 'ended': 1},
                                    format='json')
        response = self.view(request)
        invoice = Invoice.objects.get(pk=9)
        self.assertEqual(Invoice.objects.count(), 1)
        self.assertEqual(response.data['status'], 'OK')
        self.assertEqual(response.data['invoice']['invoice_id'], invoice.invoice_id)
        self.assertEqual(response.data['invoice']['receipt']['receipt_id'], self.receipt.receipt_id)
        self.assertEqual(response.data['invoice']['receipt']['transaction']['transaction_id'],
                         self.transaction.transaction_id)
        self.assertFalse(response.data['invoice']['ended'])

        invoice.delete()
        request = self.factory.post('create_invoice', {'receipt_id': self.receipt.receipt_id, 'ended': 0},
                                    format='json')
        response = self.view(request)
        invoice = Invoice.objects.get(pk=10)
        self.assertEqual(Invoice.objects.count(), 1)
        self.assertEqual(response.data['status'], 'OK')
        self.assertEqual(response.data['invoice']['invoice_id'], invoice.invoice_id)
        self.assertEqual(response.data['invoice']['receipt']['receipt_id'], self.receipt.receipt_id)
        self.assertEqual(response.data['invoice']['receipt']['transaction']['transaction_id'],
                         self.transaction.transaction_id)
        self.assertFalse(response.data['invoice']['ended'])

        invoice.delete()
        request = self.factory.post('create_invoice', {'receipt_id': self.receipt.receipt_id, 'ended': -1},
                                    format='json')
        response = self.view(request)
        invoice = Invoice.objects.get(pk=11)
        self.assertEqual(Invoice.objects.count(), 1)
        self.assertEqual(response.data['status'], 'OK')
        self.assertEqual(response.data['invoice']['invoice_id'], invoice.invoice_id)
        self.assertEqual(response.data['invoice']['receipt']['receipt_id'], self.receipt.receipt_id)
        self.assertEqual(response.data['invoice']['receipt']['transaction']['transaction_id'],
                         self.transaction.transaction_id)
        self.assertFalse(response.data['invoice']['ended'])

        invoice.delete()
        request = self.factory.post('create_invoice', {'receipt_id': self.receipt.receipt_id, 'ended': 1.1},
                                    format='json')
        response = self.view(request)
        invoice = Invoice.objects.get(pk=12)
        self.assertEqual(Invoice.objects.count(), 1)
        self.assertEqual(response.data['status'], 'OK')
        self.assertEqual(response.data['invoice']['invoice_id'], invoice.invoice_id)
        self.assertEqual(response.data['invoice']['receipt']['receipt_id'], self.receipt.receipt_id)
        self.assertEqual(response.data['invoice']['receipt']['transaction']['transaction_id'],
                         self.transaction.transaction_id)
        self.assertFalse(response.data['invoice']['ended'])

        invoice.delete()
        request = self.factory.post('create_invoice', {'receipt_id': self.receipt.receipt_id, 'ended': -1.1},
                                    format='json')
        response = self.view(request)
        invoice = Invoice.objects.get(pk=13)
        self.assertEqual(Invoice.objects.count(), 1)
        self.assertEqual(response.data['status'], 'OK')
        self.assertEqual(response.data['invoice']['invoice_id'], invoice.invoice_id)
        self.assertEqual(response.data['invoice']['receipt']['receipt_id'], self.receipt.receipt_id)
        self.assertEqual(response.data['invoice']['receipt']['transaction']['transaction_id'],
                         self.transaction.transaction_id)
        self.assertFalse(response.data['invoice']['ended'])

        invoice.delete()
        request = self.factory.post('create_invoice', {'receipt_id': self.receipt.receipt_id, 'ended': None},
                                    format='json')
        response = self.view(request)
        invoice = Invoice.objects.get(pk=14)
        self.assertEqual(Invoice.objects.count(), 1)
        self.assertEqual(response.data['status'], 'OK')
        self.assertEqual(response.data['invoice']['invoice_id'], invoice.invoice_id)
        self.assertEqual(response.data['invoice']['receipt']['receipt_id'], self.receipt.receipt_id)
        self.assertEqual(response.data['invoice']['receipt']['transaction']['transaction_id'],
                         self.transaction.transaction_id)
        self.assertFalse(response.data['invoice']['ended'])

        invoice.delete()
        request = self.factory.post('create_invoice', {'receipt_id': self.receipt.receipt_id, 'ended': list()},
                                    format='json')
        response = self.view(request)
        invoice = Invoice.objects.get(pk=15)
        self.assertEqual(Invoice.objects.count(), 1)
        self.assertEqual(response.data['status'], 'OK')
        self.assertEqual(response.data['invoice']['invoice_id'], invoice.invoice_id)
        self.assertEqual(response.data['invoice']['receipt']['receipt_id'], self.receipt.receipt_id)
        self.assertEqual(response.data['invoice']['receipt']['transaction']['transaction_id'],
                         self.transaction.transaction_id)
        self.assertFalse(response.data['invoice']['ended'])

        invoice.delete()
        request = self.factory.post('create_invoice', {'receipt_id': self.receipt.receipt_id, 'ended': tuple()},
                                    format='json')
        response = self.view(request)
        invoice = Invoice.objects.get(pk=16)
        self.assertEqual(Invoice.objects.count(), 1)
        self.assertEqual(response.data['status'], 'OK')
        self.assertEqual(response.data['invoice']['invoice_id'], invoice.invoice_id)
        self.assertEqual(response.data['invoice']['receipt']['receipt_id'], self.receipt.receipt_id)
        self.assertEqual(response.data['invoice']['receipt']['transaction']['transaction_id'],
                         self.transaction.transaction_id)
        self.assertFalse(response.data['invoice']['ended'])

        invoice.delete()
        request = self.factory.post('create_invoice', {'receipt_id': self.receipt.receipt_id, 'ended': dict()},
                                    format='json')
        response = self.view(request)
        invoice = Invoice.objects.get(pk=17)
        self.assertEqual(Invoice.objects.count(), 1)
        self.assertEqual(response.data['status'], 'OK')
        self.assertEqual(response.data['invoice']['invoice_id'], invoice.invoice_id)
        self.assertEqual(response.data['invoice']['receipt']['receipt_id'], self.receipt.receipt_id)
        self.assertEqual(response.data['invoice']['receipt']['transaction']['transaction_id'],
                         self.transaction.transaction_id)
        self.assertFalse(response.data['invoice']['ended'])

        invoice.delete()
        request = self.factory.post('create_invoice', {'receipt_id': self.receipt.receipt_id, 'ended': set()},
                                    format='json')
        response = self.view(request)
        invoice = Invoice.objects.get(pk=18)
        self.assertEqual(Invoice.objects.count(), 1)
        self.assertEqual(response.data['status'], 'OK')
        self.assertEqual(response.data['invoice']['invoice_id'], invoice.invoice_id)
        self.assertEqual(response.data['invoice']['receipt']['receipt_id'], self.receipt.receipt_id)
        self.assertEqual(response.data['invoice']['receipt']['transaction']['transaction_id'],
                         self.transaction.transaction_id)
        self.assertFalse(response.data['invoice']['ended'])
