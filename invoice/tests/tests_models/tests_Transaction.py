from django.test import TestCase
from ...models import Address, Company, Customer, Tax, Item, SoldItem, Transaction, Marketplace


class TestTransaction(TestCase):
    def setUp(self):
        company_address = Address.create(country='Poland', city='Warsaw', postal_code='10-100', street='Street',
                                         building_number=3, apartment_number=5)
        customer_address = Address.create(country='Poland', city='Cracow', postal_code='20-002', street='Street',
                                          building_number=1, apartment_number=23)
        self.vendor = Company.create(name='Company', address=company_address)
        self.customer = Customer.create(name='Customer', address=customer_address)
        self.marketplace = Marketplace()
        self.marketplace.save()
        self.country_code = 'pl'

    def test_create_transaction(self):
        transaction = Transaction.create(vendor=self.vendor, customer=self.customer, marketplace=self.marketplace,
                                         country_code=self.country_code)
        self.assertIsInstance(transaction, Transaction)
        self.assertEqual(transaction.vendor, self.vendor)
        self.assertEqual(transaction.customer, self.customer)
        self.assertEqual(transaction.marketplace, self.marketplace)
        self.assertEqual(transaction.country_code, self.country_code)
        self.assertFalse(transaction.refund)
        self.assertFalse(transaction.adjustment)
        self.assertEqual(Transaction.objects.count(), 1)

    def test_create_transaction_with_not_Company_as_vendor(self):
        self.assertRaises(TypeError, Transaction.create, vendor='', customer=self.customer,
                          marketplace=self.marketplace, country_code=self.country_code)

        self.assertRaises(TypeError, Transaction.create, vendor=' ', customer=self.customer,
                          marketplace=self.marketplace, country_code=self.country_code)

        self.assertRaises(TypeError, Transaction.create, vendor='1', customer=self.customer,
                          marketplace=self.marketplace, country_code=self.country_code)

        self.assertRaises(TypeError, Transaction.create, vendor='0', customer=self.customer,
                          marketplace=self.marketplace, country_code=self.country_code)

        self.assertRaises(TypeError, Transaction.create, vendor='-1', customer=self.customer,
                          marketplace=self.marketplace, country_code=self.country_code)

        self.assertRaises(TypeError, Transaction.create, vendor='1.1', customer=self.customer,
                          marketplace=self.marketplace, country_code=self.country_code)

        self.assertRaises(TypeError, Transaction.create, vendor='-1.1', customer=self.customer,
                          marketplace=self.marketplace, country_code=self.country_code)

        self.assertRaises(TypeError, Transaction.create, vendor='Text', customer=self.customer,
                          marketplace=self.marketplace, country_code=self.country_code)

        self.assertRaises(TypeError, Transaction.create, vendor=1, customer=self.customer,
                          marketplace=self.marketplace, country_code=self.country_code)

        self.assertRaises(TypeError, Transaction.create, vendor=0, customer=self.customer,
                          marketplace=self.marketplace, country_code=self.country_code)

        self.assertRaises(TypeError, Transaction.create, vendor=-1, customer=self.customer,
                          marketplace=self.marketplace, country_code=self.country_code)

        self.assertRaises(TypeError, Transaction.create, vendor=1.1, customer=self.customer,
                          marketplace=self.marketplace, country_code=self.country_code)

        self.assertRaises(TypeError, Transaction.create, vendor=-1.1, customer=self.customer,
                          marketplace=self.marketplace, country_code=self.country_code)

        self.assertRaises(TypeError, Transaction.create, vendor=True, customer=self.customer,
                          marketplace=self.marketplace, country_code=self.country_code)

        self.assertRaises(TypeError, Transaction.create, vendor=False, customer=self.customer,
                          marketplace=self.marketplace, country_code=self.country_code)

        self.assertRaises(TypeError, Transaction.create, vendor=None, customer=self.customer,
                          marketplace=self.marketplace, country_code=self.country_code)

        self.assertRaises(TypeError, Transaction.create, vendor=list(), customer=self.customer,
                          marketplace=self.marketplace, country_code=self.country_code)

        self.assertRaises(TypeError, Transaction.create, vendor=tuple(), customer=self.customer,
                          marketplace=self.marketplace, country_code=self.country_code)

        self.assertRaises(TypeError, Transaction.create, vendor=dict(), customer=self.customer,
                          marketplace=self.marketplace, country_code=self.country_code)

        self.assertRaises(TypeError, Transaction.create, vendor=set(), customer=self.customer,
                          marketplace=self.marketplace, country_code=self.country_code)
        self.assertEqual(Transaction.objects.count(), 0)

    def test_create_transaction_with_not_Customer_as_customer(self):
        self.assertRaises(TypeError, Transaction.create, vendor=self.vendor, customer='', marketplace=self.marketplace,
                          country_code=self.country_code)

        self.assertRaises(TypeError, Transaction.create, vendor=self.vendor, customer=' ', marketplace=self.marketplace,
                          country_code=self.country_code)

        self.assertRaises(TypeError, Transaction.create, vendor=self.vendor, customer='1', marketplace=self.marketplace,
                          country_code=self.country_code)

        self.assertRaises(TypeError, Transaction.create, vendor=self.vendor, customer='0', marketplace=self.marketplace,
                          country_code=self.country_code)

        self.assertRaises(TypeError, Transaction.create, vendor=self.vendor, customer='-1',
                          marketplace=self.marketplace, country_code=self.country_code)

        self.assertRaises(TypeError, Transaction.create, vendor=self.vendor, customer='1.1',
                          marketplace=self.marketplace, country_code=self.country_code)

        self.assertRaises(TypeError, Transaction.create, vendor=self.vendor, customer='-1.1',
                          marketplace=self.marketplace, country_code=self.country_code)

        self.assertRaises(TypeError, Transaction.create, vendor=self.vendor, customer=1, marketplace=self.marketplace,
                          country_code=self.country_code)

        self.assertRaises(TypeError, Transaction.create, vendor=self.vendor, customer=0, marketplace=self.marketplace,
                          country_code=self.country_code)

        self.assertRaises(TypeError, Transaction.create, vendor=self.vendor, customer=-1, marketplace=self.marketplace,
                          country_code=self.country_code)

        self.assertRaises(TypeError, Transaction.create, vendor=self.vendor, customer=1.1, marketplace=self.marketplace,
                          country_code=self.country_code)

        self.assertRaises(TypeError, Transaction.create, vendor=self.vendor, customer=-1.1,
                          marketplace=self.marketplace, country_code=self.country_code)

        self.assertRaises(TypeError, Transaction.create, vendor=self.vendor, customer=True,
                          marketplace=self.marketplace, country_code=self.country_code)

        self.assertRaises(TypeError, Transaction.create, vendor=self.vendor, customer=False,
                          marketplace=self.marketplace, country_code=self.country_code)

        self.assertRaises(TypeError, Transaction.create, vendor=self.vendor, customer=None,
                          marketplace=self.marketplace, country_code=self.country_code)

        self.assertRaises(TypeError, Transaction.create, vendor=self.vendor, customer=list(),
                          marketplace=self.marketplace, country_code=self.country_code)

        self.assertRaises(TypeError, Transaction.create, vendor=self.vendor, customer=tuple(),
                          marketplace=self.marketplace, country_code=self.country_code)

        self.assertRaises(TypeError, Transaction.create, vendor=self.vendor, customer=dict(),
                          marketplace=self.marketplace, country_code=self.country_code)

        self.assertRaises(TypeError, Transaction.create, vendor=self.vendor, customer=set(),
                          marketplace=self.marketplace, country_code=self.country_code)
        self.assertEqual(Transaction.objects.count(), 0)

    def test_create_transaction_with_not_Marketplace_as_marketplace(self):
        self.assertRaises(TypeError, Transaction.create, vendor=self.vendor, customer=self.customer, marketplace='',
                          country_code=self.country_code)

        self.assertRaises(TypeError, Transaction.create, vendor=self.vendor, customer=self.customer, marketplace=' ',
                          country_code=self.country_code)

        self.assertRaises(TypeError, Transaction.create, vendor=self.vendor, customer=self.customer, marketplace='1',
                          country_code=self.country_code)

        self.assertRaises(TypeError, Transaction.create, vendor=self.vendor, customer=self.customer, marketplace='0',
                          country_code=self.country_code)

        self.assertRaises(TypeError, Transaction.create, vendor=self.vendor, customer=self.customer, marketplace='-1',
                          country_code=self.country_code)

        self.assertRaises(TypeError, Transaction.create, vendor=self.vendor, customer=self.customer, marketplace='1.1',
                          country_code=self.country_code)

        self.assertRaises(TypeError, Transaction.create, vendor=self.vendor, customer=self.customer, marketplace='-1.1',
                          country_code=self.country_code)

        self.assertRaises(TypeError, Transaction.create, vendor=self.vendor, customer=self.customer, marketplace='Text',
                          country_code=self.country_code)

        self.assertRaises(TypeError, Transaction.create, vendor=self.vendor, customer=self.customer, marketplace=1,
                          country_code=self.country_code)

        self.assertRaises(TypeError, Transaction.create, vendor=self.vendor, customer=self.customer, marketplace=-1,
                          country_code=self.country_code)

        self.assertRaises(TypeError, Transaction.create, vendor=self.vendor, customer=self.customer, marketplace=1.1,
                          country_code=self.country_code)

        self.assertRaises(TypeError, Transaction.create, vendor=self.vendor, customer=self.customer, marketplace=-1.1,
                          country_code=self.country_code)

        self.assertRaises(TypeError, Transaction.create, vendor=self.vendor, customer=self.customer, marketplace=True,
                          country_code=self.country_code)

        self.assertRaises(TypeError, Transaction.create, vendor=self.vendor, customer=self.customer, marketplace=False,
                          country_code=self.country_code)

        self.assertRaises(TypeError, Transaction.create, vendor=self.vendor, customer=self.customer, marketplace=None,
                          country_code=self.country_code)

        self.assertRaises(TypeError, Transaction.create, vendor=self.vendor, customer=self.customer, marketplace=list(),
                          country_code=self.country_code)

        self.assertRaises(TypeError, Transaction.create, vendor=self.vendor, customer=self.customer,
                          marketplace=tuple(), country_code=self.country_code)

        self.assertRaises(TypeError, Transaction.create, vendor=self.vendor, customer=self.customer, marketplace=dict(),
                          country_code=self.country_code)

        self.assertRaises(TypeError, Transaction.create, vendor=self.vendor, customer=self.customer, marketplace=set(),
                          country_code=self.country_code)
        self.assertEqual(Transaction.objects.count(), 0)

    def test_create_transaction_with_not_string_as_country_code(self):
        self.assertRaises(TypeError, Transaction.create, vendor=self.vendor, customer=self.customer,
                          marketplace=self.marketplace, country_code=1)

        self.assertRaises(TypeError, Transaction.create, vendor=self.vendor, customer=self.customer,
                          marketplace=self.marketplace, country_code=0)

        self.assertRaises(TypeError, Transaction.create, vendor=self.vendor, customer=self.customer,
                          marketplace=self.marketplace, country_code=-1)

        self.assertRaises(TypeError, Transaction.create, vendor=self.vendor, customer=self.customer,
                          marketplace=self.marketplace, country_code=1.1)

        self.assertRaises(TypeError, Transaction.create, vendor=self.vendor, customer=self.customer,
                          marketplace=self.marketplace, country_code=-1.1)

        self.assertRaises(TypeError, Transaction.create, vendor=self.vendor, customer=self.customer,
                          marketplace=self.marketplace, country_code=True)

        self.assertRaises(TypeError, Transaction.create, vendor=self.vendor, customer=self.customer,
                          marketplace=self.marketplace, country_code=False)

        self.assertRaises(TypeError, Transaction.create, vendor=self.vendor, customer=self.customer,
                          marketplace=self.marketplace, country_code=None)

        self.assertRaises(TypeError, Transaction.create, vendor=self.vendor, customer=self.customer,
                          marketplace=self.marketplace, country_code=list())

        self.assertRaises(TypeError, Transaction.create, vendor=self.vendor, customer=self.customer,
                          marketplace=self.marketplace, country_code=tuple())

        self.assertRaises(TypeError, Transaction.create, vendor=self.vendor, customer=self.customer,
                          marketplace=self.marketplace, country_code=dict())

        self.assertRaises(TypeError, Transaction.create, vendor=self.vendor, customer=self.customer,
                          marketplace=self.marketplace, country_code=set())
        self.assertEqual(Transaction.objects.count(), 0)

    def test_create_transaction_with_too_long_country_code(self):
        self.assertRaises(TypeError, Transaction.create, vendor=self.vendor, customer=self.customer,
                          marketplace=self.marketplace, country_code='123')
        self.assertEqual(Transaction.objects.count(), 0)

    def test_create_transaction_with_empty_country_code(self):
        self.assertRaises(TypeError, Transaction.create, vendor=self.vendor, customer=self.customer,
                          marketplace=self.marketplace, country_code='')

        self.assertRaises(TypeError, Transaction.create, vendor=self.vendor, customer=self.customer,
                          marketplace=self.marketplace, country_code=' ')
        self.assertEqual(Transaction.objects.count(), 0)

    def test_create_transaction_with_not_bool_as_adjustment(self):
        self.assertRaises(TypeError, Transaction.create, vendor=self.vendor, customer=self.customer,
                          marketplace=self.marketplace, country_code=self.country_code, adjustment='')

        self.assertRaises(TypeError, Transaction.create, vendor=self.vendor, customer=self.customer,
                          marketplace=self.marketplace, country_code=self.country_code, adjustment=' ')

        self.assertRaises(TypeError, Transaction.create, vendor=self.vendor, customer=self.customer,
                          marketplace=self.marketplace, country_code=self.country_code, adjustment='1')

        self.assertRaises(TypeError, Transaction.create, vendor=self.vendor, customer=self.customer,
                          marketplace=self.marketplace, country_code=self.country_code, adjustment='0')

        self.assertRaises(TypeError, Transaction.create, vendor=self.vendor, customer=self.customer,
                          marketplace=self.marketplace, country_code=self.country_code, adjustment='-1')

        self.assertRaises(TypeError, Transaction.create, vendor=self.vendor, customer=self.customer,
                          marketplace=self.marketplace, country_code=self.country_code, adjustment='1.1')

        self.assertRaises(TypeError, Transaction.create, vendor=self.vendor, customer=self.customer,
                          marketplace=self.marketplace, country_code=self.country_code, adjustment='-1.1')

        self.assertRaises(TypeError, Transaction.create, vendor=self.vendor, customer=self.customer,
                          marketplace=self.marketplace, country_code=self.country_code, adjustment='Text')

        self.assertRaises(TypeError, Transaction.create, vendor=self.vendor, customer=self.customer,
                          marketplace=self.marketplace, country_code=self.country_code, adjustment=1)

        self.assertRaises(TypeError, Transaction.create, vendor=self.vendor, customer=self.customer,
                          marketplace=self.marketplace, country_code=self.country_code, adjustment=0)

        self.assertRaises(TypeError, Transaction.create, vendor=self.vendor, customer=self.customer,
                          marketplace=self.marketplace, country_code=self.country_code, adjustment=-1)

        self.assertRaises(TypeError, Transaction.create, vendor=self.vendor, customer=self.customer,
                          marketplace=self.marketplace, country_code=self.country_code, adjustment=1.1)

        self.assertRaises(TypeError, Transaction.create, vendor=self.vendor, customer=self.customer,
                          marketplace=self.marketplace, country_code=self.country_code, adjustment=-1.1)

        self.assertRaises(TypeError, Transaction.create, vendor=self.vendor, customer=self.customer,
                          marketplace=self.marketplace, country_code=self.country_code, adjustment=None)

        self.assertRaises(TypeError, Transaction.create, vendor=self.vendor, customer=self.customer,
                          marketplace=self.marketplace, country_code=self.country_code, adjustment=list())

        self.assertRaises(TypeError, Transaction.create, vendor=self.vendor, customer=self.customer,
                          marketplace=self.marketplace, country_code=self.country_code, adjustment=tuple())

        self.assertRaises(TypeError, Transaction.create, vendor=self.vendor, customer=self.customer,
                          marketplace=self.marketplace, country_code=self.country_code, adjustment=dict())

        self.assertRaises(TypeError, Transaction.create, vendor=self.vendor, customer=self.customer,
                          marketplace=self.marketplace, country_code=self.country_code, adjustment=set())
        self.assertEqual(Transaction.objects.count(), 0)

        self.assertRaises(TypeError, Transaction.create, vendor=self.vendor, customer=self.customer,
                          marketplace=self.marketplace, country_code=self.country_code, adjusment='')

    def test_create_transaction_with_not_bool_as_refund(self):
        self.assertRaises(TypeError, Transaction.create, vendor=self.vendor, customer=self.customer,
                          marketplace=self.marketplace, country_code=self.country_code, refund='')

        self.assertRaises(TypeError, Transaction.create, vendor=self.vendor, customer=self.customer,
                          marketplace=self.marketplace, country_code=self.country_code, refund='1')

        self.assertRaises(TypeError, Transaction.create, vendor=self.vendor, customer=self.customer,
                          marketplace=self.marketplace, country_code=self.country_code, refund='0')

        self.assertRaises(TypeError, Transaction.create, vendor=self.vendor, customer=self.customer,
                          marketplace=self.marketplace, country_code=self.country_code, refund='-1')

        self.assertRaises(TypeError, Transaction.create, vendor=self.vendor, customer=self.customer,
                          marketplace=self.marketplace, country_code=self.country_code, refund='1.1')

        self.assertRaises(TypeError, Transaction.create, vendor=self.vendor, customer=self.customer,
                          marketplace=self.marketplace, country_code=self.country_code, refund='-1.1')

        self.assertRaises(TypeError, Transaction.create, vendor=self.vendor, customer=self.customer,
                          marketplace=self.marketplace, country_code=self.country_code, refund='Text')

        self.assertRaises(TypeError, Transaction.create, vendor=self.vendor, customer=self.customer,
                          marketplace=self.marketplace, country_code=self.country_code, refund=1)

        self.assertRaises(TypeError, Transaction.create, vendor=self.vendor, customer=self.customer,
                          marketplace=self.marketplace, country_code=self.country_code, refund=0)

        self.assertRaises(TypeError, Transaction.create, vendor=self.vendor, customer=self.customer,
                          marketplace=self.marketplace, country_code=self.country_code, refund=-1)

        self.assertRaises(TypeError, Transaction.create, vendor=self.vendor, customer=self.customer,
                          marketplace=self.marketplace, country_code=self.country_code, refund=1.1)

        self.assertRaises(TypeError, Transaction.create, vendor=self.vendor, customer=self.customer,
                          marketplace=self.marketplace, country_code=self.country_code, refund=-1.1)

        self.assertRaises(TypeError, Transaction.create, vendor=self.vendor, customer=self.customer,
                          marketplace=self.marketplace, country_code=self.country_code, refund=None)

        self.assertRaises(TypeError, Transaction.create, vendor=self.vendor, customer=self.customer,
                          marketplace=self.marketplace, country_code=self.country_code, refund=list())

        self.assertRaises(TypeError, Transaction.create, vendor=self.vendor, customer=self.customer,
                          marketplace=self.marketplace, country_code=self.country_code, refund=tuple())

        self.assertRaises(TypeError, Transaction.create, vendor=self.vendor, customer=self.customer,
                          marketplace=self.marketplace, country_code=self.country_code, refund=dict())

        self.assertRaises(TypeError, Transaction.create, vendor=self.vendor, customer=self.customer,
                          marketplace=self.marketplace, country_code=self.country_code, refund=set())
        self.assertEqual(Transaction.objects.count(), 0)

    def test_properties(self):
        transaction = Transaction.create(vendor=self.vendor, customer=self.customer, marketplace=self.marketplace,
                                         country_code=self.country_code)
        self.assertEqual(transaction.net_value, 0)
        self.assertEqual(transaction.tax_values, {})
        self.assertEqual(transaction.tax_value, 0)
        self.assertEqual(transaction.total_value, 0)
        self.assertEqual(transaction.total_earnings, 0)

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
            transaction.items.add(sold_item)

        self.assertEqual(transaction.net_value, 225.00)
        self.assertEqual(float(transaction.tax_values['Vat_0.23']), 6.9)
        self.assertEqual(float(transaction.tax_values['Vat_0.08']), 3.6)
        self.assertEqual(float(transaction.tax_values['Vat_0.05']), 3.25)
        self.assertEqual(float(transaction.tax_values['Vat_0.0']), 0)
        self.assertEqual(transaction.tax_value, 13.75)
        self.assertEqual(transaction.total_value, 238.75)
        self.assertEqual(transaction.total_earnings, 112.50)
