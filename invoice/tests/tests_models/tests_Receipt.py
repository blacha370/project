from django.test import TestCase
from ...models import Address, Company, Customer, Tax, Item, SoldItem, Transaction, Marketplace, Receipt


class ReceiptTestCase(TestCase):
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

    def test_create_receipt(self):
        receipt = Receipt.create(transaction=self.transaction)
        self.assertIsInstance(receipt, Receipt)
        self.assertEqual(receipt.transaction, self.transaction)
        self.assertEqual(Receipt.objects.count(), 1)

    def test_create_multiple_receipts_with_same_transaction(self):
        receipt = Receipt.create(transaction=self.transaction)
        self.assertIsInstance(receipt, Receipt)
        self.assertEqual(receipt.transaction, self.transaction)
        self.assertEqual(Receipt.objects.count(), 1)

        self.assertRaises(TypeError, Receipt.create, transaction=self.transaction)
        self.assertEqual(Receipt.objects.count(), 1)

    def test_create_receipt_with_transactions_without_items(self):
        for item in self.transaction.items.all():
            item.delete()

        self.assertRaises(TypeError, Receipt.create, transaction=self.transaction)
        self.assertEqual(Receipt.objects.count(), 0)

    def test_create_receipt_with_not_Transaction_as_transactio(self):
        self.assertRaises(TypeError, Receipt.create, transaction='')

        self.assertRaises(TypeError, Receipt.create, transaction='1')

        self.assertRaises(TypeError, Receipt.create, transaction='0')

        self.assertRaises(TypeError, Receipt.create, transaction='-1')

        self.assertRaises(TypeError, Receipt.create, transaction='1.1')

        self.assertRaises(TypeError, Receipt.create, transaction='-1.1')

        self.assertRaises(TypeError, Receipt.create, transaction='Text')

        self.assertRaises(TypeError, Receipt.create, transaction=1)

        self.assertRaises(TypeError, Receipt.create, transaction=0)

        self.assertRaises(TypeError, Receipt.create, transaction=-1)

        self.assertRaises(TypeError, Receipt.create, transaction=1.1)

        self.assertRaises(TypeError, Receipt.create, transaction=-1.1)

        self.assertRaises(TypeError, Receipt.create, transaction=True)

        self.assertRaises(TypeError, Receipt.create, transaction=False)

        self.assertRaises(TypeError, Receipt.create, transaction=None)

        self.assertRaises(TypeError, Receipt.create, transaction=list())

        self.assertRaises(TypeError, Receipt.create, transaction=tuple())

        self.assertRaises(TypeError, Receipt.create, transaction=dict())

        self.assertRaises(TypeError, Receipt.create, transaction=set())
        self.assertEqual(Receipt.objects.count(), 0)
