from django.test import TestCase
from ...models import Tax, Item, SoldItem


class SoldItemTestCase(TestCase):
    def setUp(self):
        tax = Tax.create(0.23)
        self.item = Item.create(title='Item', name='Item name', price=9.99, category=1, earnings=8.15,
                                subscription_term=2, vat=tax)

    def test_create_sold_item(self):
        item = SoldItem.create(item=self.item, units=1)
        self.assertIsInstance(item, SoldItem)
        self.assertEqual(item.item, self.item)
        self.assertEqual(item.units, 1)
        self.assertEqual(item.trial, False)
        self.assertEqual(SoldItem.objects.count(), 1)

    def test_create_sold_item_with_trial(self):
        item = SoldItem.create(item=self.item, units=1, trial=False)
        self.assertIsInstance(item, SoldItem)
        self.assertEqual(item.item, self.item)
        self.assertEqual(item.units, 1)
        self.assertEqual(item.trial, False)
        self.assertEqual(SoldItem.objects.count(), 1)

        item = SoldItem.create(item=self.item, units=1, trial=True)
        self.assertIsInstance(item, SoldItem)
        self.assertEqual(item.item, self.item)
        self.assertEqual(item.units, 1)
        self.assertEqual(item.trial, True)
        self.assertEqual(SoldItem.objects.count(), 2)

    def test_create_sold_item_with_trial_for_item_without_subscription_category(self):
        self.item.category = 2
        self.item.save()
        item = SoldItem.create(item=self.item, units=1, trial=False)
        self.assertIsInstance(item, SoldItem)
        self.assertEqual(item.item, self.item)
        self.assertEqual(item.units, 1)
        self.assertEqual(item.trial, None)
        self.assertEqual(SoldItem.objects.count(), 1)

        item = SoldItem.create(item=self.item, units=1, trial=True)
        self.assertIsInstance(item, SoldItem)
        self.assertEqual(item.item, self.item)
        self.assertEqual(item.units, 1)
        self.assertEqual(item.trial, None)
        self.assertEqual(SoldItem.objects.count(), 2)

    def test_create_sold_item_with_not_Item_as_item(self):
        self.assertRaises(TypeError, SoldItem.create, item='', units=1)

        self.assertRaises(TypeError, SoldItem.create, item=' ', units=1)

        self.assertRaises(TypeError, SoldItem.create, item='1', units=1)

        self.assertRaises(TypeError, SoldItem.create, item='0', units=1)

        self.assertRaises(TypeError, SoldItem.create, item='-1', units=1)

        self.assertRaises(TypeError, SoldItem.create, item='1.1', units=1)

        self.assertRaises(TypeError, SoldItem.create, item='-1.1', units=1)

        self.assertRaises(TypeError, SoldItem.create, item='Text', units=1)

        self.assertRaises(TypeError, SoldItem.create, item=1, units=1)

        self.assertRaises(TypeError, SoldItem.create, item=0, units=1)

        self.assertRaises(TypeError, SoldItem.create, item=-1, units=1)

        self.assertRaises(TypeError, SoldItem.create, item=1.1, units=1)

        self.assertRaises(TypeError, SoldItem.create, item=-1.1, units=1)

        self.assertRaises(TypeError, SoldItem.create, item=True, units=1)

        self.assertRaises(TypeError, SoldItem.create, item=False, units=1)

        self.assertRaises(TypeError, SoldItem.create, item=None, units=1)

        self.assertRaises(TypeError, SoldItem.create, item=list(), units=1)

        self.assertRaises(TypeError, SoldItem.create, item=tuple(), units=1)

        self.assertRaises(TypeError, SoldItem.create, item=dict(), units=1)

        self.assertRaises(TypeError, SoldItem.create, item=set(), units=1)
        self.assertEqual(SoldItem.objects.count(), 0)

    def test_create_sold_item_with_not_int_as_units(self):
        self.assertRaises(TypeError, SoldItem.create, item=self.item, units='')

        self.assertRaises(TypeError, SoldItem.create, item=self.item, units=' ')

        self.assertRaises(TypeError, SoldItem.create, item=self.item, units='1')

        self.assertRaises(TypeError, SoldItem.create, item=self.item, units='0')

        self.assertRaises(TypeError, SoldItem.create, item=self.item, units='-1')

        self.assertRaises(TypeError, SoldItem.create, item=self.item, units='1.1')

        self.assertRaises(TypeError, SoldItem.create, item=self.item, units='-1.1')

        self.assertRaises(TypeError, SoldItem.create, item=self.item, units='Text')

        self.assertRaises(TypeError, SoldItem.create, item=self.item, units=1.1)

        self.assertRaises(TypeError, SoldItem.create, item=self.item, units=-1.1)

        self.assertRaises(TypeError, SoldItem.create, item=self.item, units=True)

        self.assertRaises(TypeError, SoldItem.create, item=self.item, units=False)

        self.assertRaises(TypeError, SoldItem.create, item=self.item, units=None)

        self.assertRaises(TypeError, SoldItem.create, item=self.item, units=list())

        self.assertRaises(TypeError, SoldItem.create, item=self.item, units=tuple())

        self.assertRaises(TypeError, SoldItem.create, item=self.item, units=dict())

        self.assertRaises(TypeError, SoldItem.create, item=self.item, units=set())
        self.assertEqual(SoldItem.objects.count(), 0)

    def test_create_sold_item_with_negative_int_or_0_as_amount(self):
        self.assertRaises(TypeError, SoldItem.create, item=self.item, units=0)

        self.assertRaises(TypeError, SoldItem.create, item=self.item, units=-1)
        self.assertEqual(SoldItem.objects.count(), 0)

    def test_crate_sold_item_with_not_bool_or_none_as_trial(self):
        self.assertRaises(TypeError, SoldItem.create, item=self.item, units=1, trial='')

        self.assertRaises(TypeError, SoldItem.create, item=self.item, units=1, trial=' ')

        self.assertRaises(TypeError, SoldItem.create, item=self.item, units=1, trial='1')

        self.assertRaises(TypeError, SoldItem.create, item=self.item, units=1, trial='0')

        self.assertRaises(TypeError, SoldItem.create, item=self.item, units=1, trial='-1')

        self.assertRaises(TypeError, SoldItem.create, item=self.item, units=1, trial='1.1')

        self.assertRaises(TypeError, SoldItem.create, item=self.item, units=1, trial='-1.1')

        self.assertRaises(TypeError, SoldItem.create, item=self.item, units=1, trial='Text')

        self.assertRaises(TypeError, SoldItem.create, item=self.item, units=1, trial=1)

        self.assertRaises(TypeError, SoldItem.create, item=self.item, units=1, trial=0)

        self.assertRaises(TypeError, SoldItem.create, item=self.item, units=1, trial=-1)

        self.assertRaises(TypeError, SoldItem.create, item=self.item, units=1, trial=1.1)

        self.assertRaises(TypeError, SoldItem.create, item=self.item, units=1, trial=-1.1)

        self.assertRaises(TypeError, SoldItem.create, item=self.item, units=1, trial=list())

        self.assertRaises(TypeError, SoldItem.create, item=self.item, units=1, trial=tuple())

        self.assertRaises(TypeError, SoldItem.create, item=self.item, units=1, trial=dict())

        self.assertRaises(TypeError, SoldItem.create, item=self.item, units=1, trial=set())
        self.assertEqual(SoldItem.objects.count(), 0)

    def test_properties(self):
        item = SoldItem.create(item=self.item, units=2)
        self.assertEqual(item.net_value, 19.98)

        self.assertEqual(item.vat_value, {'name': 'Vat_0.23',
                                          'value': 4.6})

        self.assertEqual(item.total_value, 24.58)

        self.assertEqual(item.total_earnings, 16.3)
