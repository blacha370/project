from rest_framework.test import APITestCase, APIRequestFactory
from ...views import (EndInvoice, AdvanceInvoice, Invoice, Receipt, Transaction, Company, Customer, Marketplace,
                      SoldItem, Item, Tax, Address)


class EndInvoiceTestCase(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = EndInvoice.as_view()
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

    def test_end_invoice(self):
        self.assertFalse(self.invoice.ended)
        request = self.factory.post('end_invoice', {'invoice_id': self.invoice.invoice_id}, format='json')
        response = self.view(request)
        self.assertEqual(response.data['status'], 'OK')
        self.assertEqual(response.data['invoice']['invoice_id'], self.invoice.invoice_id)
        self.assertTrue(Invoice.objects.get(invoice_id=self.invoice.invoice_id).ended)

    def test_end_invoice_with_advance_invoices(self):
        AdvanceInvoice.create(invoice=self.invoice, payment=10)
        self.assertFalse(self.invoice.ended)
        request = self.factory.post('end_invoice', {'invoice_id': self.invoice.invoice_id}, format='json')
        response = self.view(request)
        self.assertEqual(response.data['status'], 'OK')
        self.assertEqual(response.data['invoice']['invoice_id'], self.invoice.invoice_id)
        self.assertIsInstance(response.data['advance_invoices'], list)
        self.assertTrue(Invoice.objects.get(invoice_id=self.invoice.invoice_id).ended)

    def test_end_invoice_twice(self):
        self.assertFalse(self.invoice.ended)
        request = self.factory.post('end_invoice', {'invoice_id': self.invoice.invoice_id}, format='json')
        response = self.view(request)
        self.assertEqual(response.data['status'], 'OK')
        self.assertEqual(response.data['invoice']['invoice_id'], self.invoice.invoice_id)
        self.assertTrue(Invoice.objects.get(invoice_id=self.invoice.invoice_id).ended)

        request = self.factory.post('end_invoice', {'invoice_id': self.invoice.invoice_id}, format='json')
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Invoice is already ended')

    def test_end_invoice_with_not_string_as_invoice_id(self):
        request = self.factory.post('end_invoice', {'invoice_id': 1}, format='json')
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Invoice with provided invoice_id does not exist')

        request = self.factory.post('end_invoice', {'invoice_id': 0}, format='json')
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Invoice with provided invoice_id does not exist')

        request = self.factory.post('end_invoice', {'invoice_id': -1}, format='json')
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Invoice with provided invoice_id does not exist')

        request = self.factory.post('end_invoice', {'invoice_id': 1.1}, format='json')
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Invoice with provided invoice_id does not exist')

        request = self.factory.post('end_invoice', {'invoice_id': -1.1}, format='json')
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Invoice with provided invoice_id does not exist')

        request = self.factory.post('end_invoice', {'invoice_id': True}, format='json')
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Invoice with provided invoice_id does not exist')

        request = self.factory.post('end_invoice', {'invoice_id': False}, format='json')
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Invoice with provided invoice_id does not exist')

        request = self.factory.post('end_invoice', {'invoice_id': None}, format='json')
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Invoice with provided invoice_id does not exist')

        request = self.factory.post('end_invoice', {'invoice_id': list()}, format='json')
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Invoice with provided invoice_id does not exist')

        request = self.factory.post('end_invoice', {'invoice_id': tuple()}, format='json')
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Invoice with provided invoice_id does not exist')

        request = self.factory.post('end_invoice', {'invoice_id': dict()}, format='json')
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Invoice with provided invoice_id does not exist')

        request = self.factory.post('end_invoice', {'invoice_id': set()}, format='json')
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Invoice with provided invoice_id does not exist')

    def test_end_invoice_with_empty_string_as_invoice_id(self):
        request = self.factory.post('end_invoice', {'invoice_id': ''}, format='json')
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Invoice with provided invoice_id does not exist')

    def test_end_invoice_without_invoice_id(self):
        request = self.factory.post('end_invoice', {}, format='json')
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'missing argument: invoice_id')
