from django.test import TestCase
from ...models import Address, Company, Customer, Tax, Item, SoldItem, Transaction, Marketplace, Receipt, Invoice, \
    AdvanceInvoice


class AdvanceInvoiceTestCase(TestCase):
    def setUp(self):
        company_address = Address.create(country='Poland', city='Warsaw', postal_code='10-100', street='Street',
                                         building_number=3, apartment_number=5)
        customer_address = Address.create(country='Poland', city='Cracow', postal_code='20-002', street='Street',
                                          building_number=1, apartment_number=23)
        vendor = Company.create(name='Company', address=company_address)
        customer = Customer.create(name='Customer', address=customer_address)
        marketplace = Marketplace()
        marketplace.save()
        country_code = 'pl'
        self.transaction = Transaction.create(vendor=vendor, customer=customer, marketplace=marketplace,
                                              country_code=country_code)
        taxes = []
        for i in (0.23, 0.08, 0.05, 0.00):
            taxes.append(Tax.create(i))
        Item.create(title='Item1', name='Item1', price=1, earnings=0.5, vat=taxes[0])
        Item.create(title='Item2', name='Item2', price=2, earnings=1, vat=taxes[0])
        Item.create(title='Item3', name='Item3', price=3, earnings=1.5, vat=taxes[0])
        Item.create(title='Item4', name='Item4', price=4, earnings=2, vat=taxes[1])
        Item.create(title='Item5', name='Item5', price=5, earnings=2.5, vat=taxes[1])
        Item.create(title='Item6', name='Item6', price=6, earnings=3, vat=taxes[2])
        Item.create(title='Item7', name='Item7', price=7, earnings=3.5, vat=taxes[2])
        Item.create(title='Item8', name='Item8', price=8, earnings=4, vat=taxes[3])
        Item.create(title='Item9', name='Item9', price=9, earnings=4.5, vat=taxes[3])
        for item in Item.objects.all():
            sold_item = SoldItem.create(item=item, units=5)
            self.transaction.items.add(sold_item)

        self.receipt = Receipt.create(transaction=self.transaction)
        self.invoice = Invoice.create(receipt=self.receipt)

    def test_create_advance_invoice(self):
        advance_invoice = AdvanceInvoice.create(invoice=self.invoice, payment=100)
        self.assertIsInstance(advance_invoice, AdvanceInvoice)
        self.assertEqual(advance_invoice.invoice, self.invoice)
        self.assertEqual(advance_invoice.advance_invoice_id, self.invoice.invoice_id + '-01')
        self.assertEqual(advance_invoice.payment, 100)
        self.assertEqual(AdvanceInvoice.objects.count(), 1)

    def test_create_advance_invoice_with_to_big_payment(self):
        self.assertRaises(TypeError, AdvanceInvoice.create, invoice=self.invoice, payment=1000)
        self.assertEqual(AdvanceInvoice.objects.count(), 0)

    def test_create_advance_invoices_until_invoice_is_ended(self):
        advance_invoice = AdvanceInvoice.create(invoice=self.invoice, payment=100)
        self.assertIsInstance(advance_invoice, AdvanceInvoice)
        self.assertEqual(advance_invoice.advance_invoice_id, self.invoice.invoice_id + '-01')
        self.assertEqual(advance_invoice.invoice, self.invoice)
        self.assertEqual(advance_invoice.payment, 100)
        self.assertEqual(AdvanceInvoice.objects.count(), 1)

        advance_invoice = AdvanceInvoice.create(invoice=self.invoice, payment=100)
        self.assertIsInstance(advance_invoice, AdvanceInvoice)
        self.assertEqual(advance_invoice.advance_invoice_id, self.invoice.invoice_id + '-02')
        self.assertEqual(advance_invoice.invoice, self.invoice)
        self.assertEqual(advance_invoice.payment, 100)
        self.assertEqual(AdvanceInvoice.objects.count(), 2)

        advance_invoice = AdvanceInvoice.create(invoice=self.invoice, payment=38.75)
        self.assertIsInstance(advance_invoice, AdvanceInvoice)
        self.assertEqual(advance_invoice.advance_invoice_id, self.invoice.invoice_id + '-03')
        self.assertEqual(advance_invoice.invoice, self.invoice)
        self.assertEqual(advance_invoice.payment, 38.75)
        self.assertEqual(AdvanceInvoice.objects.count(), 3)
        self.assertTrue(self.invoice.ended)
        self.assertIsNotNone(self.invoice.time)

    def test_create_advance_invoice_for_ended_invoice(self):
        self.invoice.end_invoice()
        self.assertRaises(TypeError, AdvanceInvoice.create, invoice=self.invoice, payment=100)
        self.assertEqual(AdvanceInvoice.objects.count(), 0)

    def test_create_advance_invoice_with_not_Invoice_as_invoice(self):
        self.assertRaises(TypeError, AdvanceInvoice.create, invoice='', payment=100)

        self.assertRaises(TypeError, AdvanceInvoice.create, invoice=' ', payment=100)

        self.assertRaises(TypeError, AdvanceInvoice.create, invoice='1', payment=100)

        self.assertRaises(TypeError, AdvanceInvoice.create, invoice='0', payment=100)

        self.assertRaises(TypeError, AdvanceInvoice.create, invoice='-1', payment=100)

        self.assertRaises(TypeError, AdvanceInvoice.create, invoice='1.1', payment=100)

        self.assertRaises(TypeError, AdvanceInvoice.create, invoice='-1.1', payment=100)

        self.assertRaises(TypeError, AdvanceInvoice.create, invoice='Text', payment=100)

        self.assertRaises(TypeError, AdvanceInvoice.create, invoice=1, payment=100)

        self.assertRaises(TypeError, AdvanceInvoice.create, invoice=0, payment=100)

        self.assertRaises(TypeError, AdvanceInvoice.create, invoice=-1, payment=100)

        self.assertRaises(TypeError, AdvanceInvoice.create, invoice=1.1, payment=100)

        self.assertRaises(TypeError, AdvanceInvoice.create, invoice=-1.1, payment=100)

        self.assertRaises(TypeError, AdvanceInvoice.create, invoice=True, payment=100)

        self.assertRaises(TypeError, AdvanceInvoice.create, invoice=False, payment=100)

        self.assertRaises(TypeError, AdvanceInvoice.create, invoice=None, payment=100)

        self.assertRaises(TypeError, AdvanceInvoice.create, invoice=list(), payment=100)

        self.assertRaises(TypeError, AdvanceInvoice.create, invoice=dict(), payment=100)

        self.assertRaises(TypeError, AdvanceInvoice.create, invoice=tuple(), payment=100)

        self.assertRaises(TypeError, AdvanceInvoice.create, invoice=set(), payment=100)
        self.assertEqual(AdvanceInvoice.objects.count(), 0)

    def test_create_invoice_with_not_int_or_float_as_payment(self):
        self.assertRaises(TypeError, AdvanceInvoice.create, invoice=self.invoice, payment='')

        self.assertRaises(TypeError, AdvanceInvoice.create, invoice=self.invoice, payment=' ')

        self.assertRaises(TypeError, AdvanceInvoice.create, invoice=self.invoice, payment='1')

        self.assertRaises(TypeError, AdvanceInvoice.create, invoice=self.invoice, payment='0')

        self.assertRaises(TypeError, AdvanceInvoice.create, invoice=self.invoice, payment='-1')

        self.assertRaises(TypeError, AdvanceInvoice.create, invoice=self.invoice, payment='Text')

        self.assertRaises(TypeError, AdvanceInvoice.create, invoice=self.invoice, payment=True)

        self.assertRaises(TypeError, AdvanceInvoice.create, invoice=self.invoice, payment=False)

        self.assertRaises(TypeError, AdvanceInvoice.create, invoice=self.invoice, payment=None)

        self.assertRaises(TypeError, AdvanceInvoice.create, invoice=self.invoice, payment=list())

        self.assertRaises(TypeError, AdvanceInvoice.create, invoice=self.invoice, payment=tuple())

        self.assertRaises(TypeError, AdvanceInvoice.create, invoice=self.invoice, payment=dict())

        self.assertRaises(TypeError, AdvanceInvoice.create, invoice=self.invoice, payment=set())
        self.assertEqual(AdvanceInvoice.objects.count(), 0)
