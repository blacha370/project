from django.test import TestCase
from ...models import Tax, Item


class ItemTestCase(TestCase):
    def setUp(self):
        self.tax = Tax.create(0.23)
        self.title = 'Item'
        self.name = 'Item name'
        self.price = 9.99
        self.category = 1
        self.earnings = 8.15
        self.subscription_term = 2

    def test_create_item(self):
        item = Item.create(title=self.title, name=self.name, price=self.price, category=self.category,
                           earnings=self.earnings, subscription_term=self.subscription_term, vat=self.tax)
        self.assertIsInstance(item, Item)
        self.assertEqual(item.title, self.title)
        self.assertEqual(item.name, self.name)
        self.assertEqual(item.price, self.price)
        self.assertEqual(item.category, self.category)
        self.assertEqual(item.earnings, self.earnings)
        self.assertEqual(item.subscription_term, self.subscription_term)
        self.assertEqual(item.vat, self.tax)
        self.assertIsInstance(item.vat, Tax)
        self.assertEqual(Item.objects.count(), 1)

    def test_create_item_with_subscription_term_and_not_subscription_category(self):
        item = Item.create(title=self.title, name=self.name, price=self.price, category=2, earnings=self.earnings,
                           subscription_term=self.subscription_term, vat=self.tax)
        self.assertIsInstance(item, Item)
        self.assertEqual(item.title, self.title)
        self.assertEqual(item.name, self.name)
        self.assertEqual(item.price, self.price)
        self.assertEqual(item.category, 2)
        self.assertEqual(item.earnings, self.earnings)
        self.assertEqual(item.subscription_term, None)
        self.assertEqual(item.vat, self.tax)
        self.assertIsInstance(item.vat, Tax)
        self.assertEqual(Item.objects.count(), 1)

    def test_create_item_without_category(self):
        item = Item.create(title=self.title, name=self.name, price=self.price, earnings=self.earnings,
                           subscription_term=self.subscription_term, vat=self.tax)
        self.assertIsInstance(item, Item)
        self.assertEqual(item.title, self.title)
        self.assertEqual(item.name, self.name)
        self.assertEqual(item.price, self.price)
        self.assertEqual(item.category, None)
        self.assertEqual(item.earnings, self.earnings)
        self.assertEqual(item.subscription_term, None)
        self.assertEqual(item.vat, self.tax)
        self.assertIsInstance(item.vat, Tax)
        self.assertEqual(Item.objects.count(), 1)

    def test_create_item_without_subscription_term(self):
        item = Item.create(title=self.title, name=self.name, price=self.price, earnings=self.earnings,
                           category=self.category, vat=self.tax)
        self.assertIsInstance(item, Item)
        self.assertEqual(item.title, self.title)
        self.assertEqual(item.name, self.name)
        self.assertEqual(item.price, self.price)
        self.assertEqual(item.category, 1)
        self.assertEqual(item.earnings, self.earnings)
        self.assertEqual(item.subscription_term, 1)
        self.assertEqual(item.vat, self.tax)
        self.assertIsInstance(item.vat, Tax)
        self.assertEqual(Item.objects.count(), 1)

    def test_create_item_without_category_and_subscription_term(self):
        item = Item.create(title=self.title, name=self.name, price=self.price, earnings=self.earnings, vat=self.tax)
        self.assertIsInstance(item, Item)
        self.assertEqual(item.title, self.title)
        self.assertEqual(item.name, self.name)
        self.assertEqual(item.price, self.price)
        self.assertEqual(item.category, None)
        self.assertEqual(item.earnings, self.earnings)
        self.assertEqual(item.subscription_term, None)
        self.assertEqual(item.vat, self.tax)
        self.assertIsInstance(item.vat, Tax)
        self.assertEqual(Item.objects.count(), 1)

    def test_create_item_with_not_string_as_title(self):
        self.assertRaises(TypeError, Item.create, title=1, name=self.name, price=self.price, category=self.category,
                          earnings=self.earnings, subscription_term=self.subscription_term, vat=self.tax)

        self.assertRaises(TypeError, Item.create, title=0, name=self.name, price=self.price, category=self.category,
                          earnings=self.earnings, subscription_term=self.subscription_term, vat=self.tax)

        self.assertRaises(TypeError, Item.create, title=-1, name=self.name, price=self.price, category=self.category,
                          earnings=self.earnings, subscription_term=self.subscription_term, vat=self.tax)

        self.assertRaises(TypeError, Item.create, title=1.1, name=self.name, price=self.price, category=self.category,
                          earnings=self.earnings, subscription_term=self.subscription_term, vat=self.tax)

        self.assertRaises(TypeError, Item.create, title=-1.1, name=self.name, price=self.price, category=self.category,
                          earnings=self.earnings, subscription_term=self.subscription_term, vat=self.tax)

        self.assertRaises(TypeError, Item.create, title=True, name=self.name, price=self.price, category=self.category,
                          earnings=self.earnings, subscription_term=self.subscription_term, vat=self.tax)

        self.assertRaises(TypeError, Item.create, title=False, name=self.name, price=self.price, category=self.category,
                          earnings=self.earnings, subscription_term=self.subscription_term, vat=self.tax)

        self.assertRaises(TypeError, Item.create, title=None, name=self.name, price=self.price, category=self.category,
                          earnings=self.earnings, subscription_term=self.subscription_term, vat=self.tax)

        self.assertRaises(TypeError, Item.create, title=list(), name=self.name, price=self.price,
                          category=self.category, earnings=self.earnings, subscription_term=self.subscription_term,
                          vat=self.tax)

        self.assertRaises(TypeError, Item.create, title=tuple(), name=self.name, price=self.price,
                          category=self.category, earnings=self.earnings, subscription_term=self.subscription_term,
                          vat=self.tax)

        self.assertRaises(TypeError, Item.create, title=dict(), name=self.name, price=self.price,
                          category=self.category, earnings=self.earnings, subscription_term=self.subscription_term,
                          vat=self.tax)

        self.assertRaises(TypeError, Item.create, title=set(), name=self.name, price=self.price, category=self.category,
                          earnings=self.earnings, subscription_term=self.subscription_term, vat=self.tax)
        self.assertEqual(Item.objects.count(), 0)

    def test_create_item_with_empty_string_as_title(self):
        self.assertRaises(TypeError, Item.create, title='', name=self.name, price=self.price,
                          category=self.category, earnings=self.earnings, subscription_term=self.subscription_term,
                          vat=self.tax)

        self.assertRaises(TypeError, Item.create, title=' ', name=self.name, price=self.price, category=self.category,
                          earnings=self.earnings, subscription_term=self.subscription_term, vat=self.tax)
        self.assertEqual(Item.objects.count(), 0)

    def test_create_item_with_too_long_title(self):
        title = '1' * 51
        self.assertRaises(TypeError, Item.create, title=title, name=self.name, price=self.price, category=self.category,
                          earnings=self.earnings, subscription_term=self.subscription_term, vat=self.tax)
        self.assertEqual(Item.objects.count(), 0)

    def test_create_item_with_not_string_as_name(self):
        self.assertRaises(TypeError, Item.create, title=self.title, name=1, price=self.price, category=self.category,
                          earnings=self.earnings, subscription_term=self.subscription_term, vat=self.tax)

        self.assertRaises(TypeError, Item.create, title=self.title, name=0, price=self.price, category=self.category,
                          earnings=self.earnings, subscription_term=self.subscription_term, vat=self.tax)

        self.assertRaises(TypeError, Item.create, title=self.title, name=-1, price=self.price, category=self.category,
                          earnings=self.earnings, subscription_term=self.subscription_term, vat=self.tax)

        self.assertRaises(TypeError, Item.create, title=self.title, name=1.1, price=self.price, category=self.category,
                          earnings=self.earnings, subscription_term=self.subscription_term, vat=self.tax)

        self.assertRaises(TypeError, Item.create, title=self.title, name=-1.1, price=self.price, category=self.category,
                          earnings=self.earnings, subscription_term=self.subscription_term, vat=self.tax)

        self.assertRaises(TypeError, Item.create, title=self.title, name=True, price=self.price, category=self.category,
                          earnings=self.earnings, subscription_term=self.subscription_term, vat=self.tax)

        self.assertRaises(TypeError, Item.create, title=self.title, name=False, price=self.price,
                          category=self.category, earnings=self.earnings, subscription_term=self.subscription_term,
                          vat=self.tax)

        self.assertRaises(TypeError, Item.create, title=self.title, name=None, price=self.price, category=self.category,
                          earnings=self.earnings, subscription_term=self.subscription_term, vat=self.tax)

        self.assertRaises(TypeError, Item.create, title=self.title, name=list(), price=self.price,
                          category=self.category, earnings=self.earnings, subscription_term=self.subscription_term,
                          vat=self.tax)

        self.assertRaises(TypeError, Item.create, title=self.title, name=tuple(), price=self.price,
                          category=self.category, earnings=self.earnings, subscription_term=self.subscription_term,
                          vat=self.tax)

        self.assertRaises(TypeError, Item.create, title=self.title, name=dict(), price=self.price,
                          category=self.category, earnings=self.earnings, subscription_term=self.subscription_term,
                          vat=self.tax)

        self.assertRaises(TypeError, Item.create, title=self.title, name=set(), price=self.price,
                          category=self.category, earnings=self.earnings, subscription_term=self.subscription_term,
                          vat=self.tax)
        self.assertEqual(Item.objects.count(), 0)

    def test_create_item_with_empty_string_as_name(self):
        self.assertRaises(TypeError, Item.create, title=self.title, name='', price=self.price, category=self.category,
                          earnings=self.earnings, subscription_term=self.subscription_term, vat=self.tax)

        self.assertRaises(TypeError, Item.create, title=self.title, name=' ', price=self.price, category=self.category,
                          earnings=self.earnings, subscription_term=self.subscription_term, vat=self.tax)
        self.assertEqual(Item.objects.count(), 0)

    def test_create_item_with_too_long_name(self):
        name = '1' * 51
        self.assertRaises(TypeError, Item.create, title=self.title, name=name, price=self.price, category=self.category,
                          earnings=self.earnings, subscription_term=self.subscription_term, vat=self.tax)
        self.assertEqual(Item.objects.count(), 0)

    def test_create_item_with_not_int_or_float_as_price(self):
        self.assertRaises(TypeError, Item.create, title=self.title, name=self.name, price='', category=self.category,
                          earnings=self.earnings, subscription_term=self.subscription_term, vat=self.tax)

        self.assertRaises(TypeError, Item.create, title=self.title, name=self.name, price=' ', category=self.category,
                          earnings=self.earnings, subscription_term=self.subscription_term, vat=self.tax)

        self.assertRaises(TypeError, Item.create, title=self.title, name=self.name, price='1', category=self.category,
                          earnings=self.earnings, subscription_term=self.subscription_term, vat=self.tax)

        self.assertRaises(TypeError, Item.create, title=self.title, name=self.name, price='0', category=self.category,
                          earnings=self.earnings, subscription_term=self.subscription_term, vat=self.tax)

        self.assertRaises(TypeError, Item.create, title=self.title, name=self.name, price='-1', category=self.category,
                          earnings=self.earnings, subscription_term=self.subscription_term, vat=self.tax)

        self.assertRaises(TypeError, Item.create, title=self.title, name=self.name, price='1.1', category=self.category,
                          earnings=self.earnings, subscription_term=self.subscription_term, vat=self.tax)

        self.assertRaises(TypeError, Item.create, title=self.title, name=self.name, price='-1.1',
                          category=self.category, earnings=self.earnings, subscription_term=self.subscription_term,
                          vat=self.tax)

        self.assertRaises(TypeError, Item.create, title=self.title, name=self.name, price='Text',
                          category=self.category, earnings=self.earnings, subscription_term=self.subscription_term,
                          vat=self.tax)

        self.assertRaises(TypeError, Item.create, title=self.title, name=self.name, price=True, category=self.category,
                          earnings=self.earnings, subscription_term=self.subscription_term, vat=self.tax)

        self.assertRaises(TypeError, Item.create, title=self.title, name=self.name, price=False, category=self.category,
                          earnings=self.earnings, subscription_term=self.subscription_term, vat=self.tax)

        self.assertRaises(TypeError, Item.create, title=self.title, name=self.name, price=None, category=self.category,
                          earnings=self.earnings, subscription_term=self.subscription_term, vat=self.tax)

        self.assertRaises(TypeError, Item.create, title=self.title, name=self.name, price=list(),
                          category=self.category, earnings=self.earnings, subscription_term=self.subscription_term,
                          vat=self.tax)

        self.assertRaises(TypeError, Item.create, title=self.title, name=self.name, price=tuple(),
                          category=self.category, earnings=self.earnings, subscription_term=self.subscription_term,
                          vat=self.tax)

        self.assertRaises(TypeError, Item.create, title=self.title, name=self.name, price=dict(),
                          category=self.category, earnings=self.earnings, subscription_term=self.subscription_term,
                          vat=self.tax)

        self.assertRaises(TypeError, Item.create, title=self.title, name=self.name, price=set(), category=self.category,
                          earnings=self.earnings, subscription_term=self.subscription_term, vat=self.tax)
        self.assertEqual(Item.objects.count(), 0)

    def test_create_item_with_negative_value_or_0_as_price(self):
        self.assertRaises(TypeError, Item.create, title=self.title, name=self.name, price=0, category=self.category,
                          earnings=self.earnings, subscription_term=self.subscription_term, vat=self.tax)

        self.assertRaises(TypeError, Item.create, title=self.title, name=self.name, price=-1, category=self.category,
                          earnings=self.earnings, subscription_term=self.subscription_term, vat=self.tax)

        self.assertRaises(TypeError, Item.create, title=self.title, name=self.name, price=-1.1, category=self.category,
                          earnings=self.earnings, subscription_term=self.subscription_term, vat=self.tax)
        self.assertEqual(Item.objects.count(), 0)

    def test_create_item_with_not_int_or_None_as_category(self):
        self.assertRaises(TypeError, Item.create, title=self.title, name=self.name, price=self.price, category='',
                          earnings=self.earnings, subscription_term=self.subscription_term, vat=self.tax)

        self.assertRaises(TypeError, Item.create, title=self.title, name=self.name, price=self.price, category=' ',
                          earnings=self.earnings, subscription_term=self.subscription_term, vat=self.tax)

        self.assertRaises(TypeError, Item.create, title=self.title, name=self.name, price=self.price, category='1',
                          earnings=self.earnings, subscription_term=self.subscription_term, vat=self.tax)

        self.assertRaises(TypeError, Item.create, title=self.title, name=self.name, price=self.price, category='0',
                          earnings=self.earnings, subscription_term=self.subscription_term, vat=self.tax)

        self.assertRaises(TypeError, Item.create, title=self.title, name=self.name, price=self.price, category='-1',
                          earnings=self.earnings, subscription_term=self.subscription_term, vat=self.tax)

        self.assertRaises(TypeError, Item.create, title=self.title, name=self.name, price=self.price, category='Text',
                          earnings=self.earnings, subscription_term=self.subscription_term, vat=self.tax)

        self.assertRaises(TypeError, Item.create, title=self.title, name=self.name, price=self.price, category=1.1,
                          earnings=self.earnings, subscription_term=self.subscription_term, vat=self.tax)

        self.assertRaises(TypeError, Item.create, title=self.title, name=self.name, price=self.price, category=-1.1,
                          earnings=self.earnings, subscription_term=self.subscription_term, vat=self.tax)

        self.assertRaises(TypeError, Item.create, title=self.title, name=self.name, price=self.price, category=True,
                          earnings=self.earnings, subscription_term=self.subscription_term, vat=self.tax)

        self.assertRaises(TypeError, Item.create, title=self.title, name=self.name, price=self.price, category=False,
                          earnings=self.earnings, subscription_term=self.subscription_term, vat=self.tax)

        self.assertRaises(TypeError, Item.create, title=self.title, name=self.name, price=self.price, category=list(),
                          earnings=self.earnings, subscription_term=self.subscription_term, vat=self.tax)

        self.assertRaises(TypeError, Item.create, title=self.title, name=self.name, price=self.price, category=tuple(),
                          earnings=self.earnings, subscription_term=self.subscription_term, vat=self.tax)

        self.assertRaises(TypeError, Item.create, title=self.title, name=self.name, price=self.price, category=dict(),
                          earnings=self.earnings, subscription_term=self.subscription_term, vat=self.tax)

        self.assertRaises(TypeError, Item.create, title=self.title, name=self.name, price=self.price, category=set(),
                          earnings=self.earnings, subscription_term=self.subscription_term, vat=self.tax)
        self.assertEqual(Item.objects.count(), 0)

    def test_create_item_with_negative_value_or_0_as_category(self):
        item = Item.create(title=self.title, name=self.name, price=self.price, category=0, earnings=self.earnings,
                           subscription_term=self.subscription_term, vat=self.tax)
        self.assertIsInstance(item, Item)
        self.assertEqual(item.title, self.title)
        self.assertEqual(item.name, self.name)
        self.assertEqual(item.price, self.price)
        self.assertEqual(item.category, None)
        self.assertEqual(item.earnings, self.earnings)
        self.assertEqual(item.subscription_term, None)
        self.assertEqual(item.vat, self.tax)
        self.assertIsInstance(item.vat, Tax)
        self.assertEqual(Item.objects.count(), 1)

        item = Item.create(title=self.title, name=self.name, price=self.price, category=-1, earnings=self.earnings,
                           subscription_term=self.subscription_term, vat=self.tax)
        self.assertIsInstance(item, Item)
        self.assertEqual(item.title, self.title)
        self.assertEqual(item.name, self.name)
        self.assertEqual(item.price, self.price)
        self.assertEqual(item.category, None)
        self.assertEqual(item.earnings, self.earnings)
        self.assertEqual(item.subscription_term, None)
        self.assertEqual(item.vat, self.tax)
        self.assertIsInstance(item.vat, Tax)
        self.assertEqual(Item.objects.count(), 2)

    def test_create_item_with_not_int_or_float_as_earnings(self):
        self.assertRaises(TypeError, Item.create, title=self.title, name=self.name, price=self.price,
                          category=self.category, earnings='', subscription_term=self.subscription_term, vat=self.tax)

        self.assertRaises(TypeError, Item.create, title=self.title, name=self.name, price=self.price,
                          category=self.category, earnings=' ', subscription_term=self.subscription_term, vat=self.tax)

        self.assertRaises(TypeError, Item.create, title=self.title, name=self.name, price=self.price,
                          category=self.category, earnings='1', subscription_term=self.subscription_term, vat=self.tax)

        self.assertRaises(TypeError, Item.create, title=self.title, name=self.name, price=self.price,
                          category=self.category, earnings='0', subscription_term=self.subscription_term, vat=self.tax)

        self.assertRaises(TypeError, Item.create, title=self.title, name=self.name, price=self.price,
                          category=self.category, earnings='-1', subscription_term=self.subscription_term, vat=self.tax)

        self.assertRaises(TypeError, Item.create, title=self.title, name=self.name, price=self.price,
                          category=self.category, earnings='1.1', subscription_term=self.subscription_term,
                          vat=self.tax)

        self.assertRaises(TypeError, Item.create, title=self.title, name=self.name, price=self.price,
                          category=self.category, earnings='-1.1', subscription_term=self.subscription_term,
                          vat=self.tax)

        self.assertRaises(TypeError, Item.create, title=self.title, name=self.name, price=self.price,
                          category=self.category, earnings='Text', subscription_term=self.subscription_term,
                          vat=self.tax)

        self.assertRaises(TypeError, Item.create, title=self.title, name=self.name, price=self.price,
                          category=self.category, earnings=True, subscription_term=self.subscription_term, vat=self.tax)

        self.assertRaises(TypeError, Item.create, title=self.title, name=self.name, price=self.price,
                          category=self.category, earnings=False, subscription_term=self.subscription_term,
                          vat=self.tax)

        self.assertRaises(TypeError, Item.create, title=self.title, name=self.name, price=self.price,
                          category=self.category, earnings=None, subscription_term=self.subscription_term, vat=self.tax)

        self.assertRaises(TypeError, Item.create, title=self.title, name=self.name, price=self.price,
                          category=self.category, earnings=list(), subscription_term=self.subscription_term,
                          vat=self.tax)

        self.assertRaises(TypeError, Item.create, title=self.title, name=self.name, price=self.price,
                          category=self.category, earnings=tuple(), subscription_term=self.subscription_term,
                          vat=self.tax)

        self.assertRaises(TypeError, Item.create, title=self.title, name=self.name, price=self.price,
                          category=self.category, earnings=dict(), subscription_term=self.subscription_term,
                          vat=self.tax)

        self.assertRaises(TypeError, Item.create, title=self.title, name=self.name, price=self.price,
                          category=self.category, earnings=set(), subscription_term=self.subscription_term,
                          vat=self.tax)
        self.assertEqual(Item.objects.count(), 0)

    def test_create_item_with_negative_or_0_as_earnings(self):
        self.assertRaises(TypeError, Item.create, title=self.title, name=self.name, price=self.price,
                          category=self.category, earnings=0, subscription_term=self.subscription_term,
                          vat=self.tax)

        self.assertRaises(TypeError, Item.create, title=self.title, name=self.name, price=self.price,
                          category=self.category, earnings=-1, subscription_term=self.subscription_term,
                          vat=self.tax)

        self.assertRaises(TypeError, Item.create, title=self.title, name=self.name, price=self.price,
                          category=self.category, earnings=-1.1, subscription_term=self.subscription_term,
                          vat=self.tax)
        self.assertEqual(Item.objects.count(), 0)

    def test_create_item_with_earnings_higher_than_price(self):
        self.assertRaises(TypeError, Item.create, title=self.title, name=self.name, price=self.price,
                          category=self.category, earnings=-self.price + 1, subscription_term=self.subscription_term,
                          vat=self.tax)
        self.assertEqual(Item.objects.count(), 0)

    def test_create_item_with_earnings_equal_to_price(self):
        self.assertRaises(TypeError, Item.create, title=self.title, name=self.name, price=self.price,
                          category=self.category, earnings=-self.price, subscription_term=self.subscription_term,
                          vat=self.tax)
        self.assertEqual(Item.objects.count(), 0)

    def test_create_item_with_not_int_as_subscription_term(self):
        self.assertRaises(TypeError, Item.create, title=self.title, name=self.name, price=self.price,
                          category=self.category, earnings=-self.earnings, subscription_term='', vat=self.tax)

        self.assertRaises(TypeError, Item.create, title=self.title, name=self.name, price=self.price,
                          category=self.category, earnings=-self.earnings, subscription_term=' ', vat=self.tax)

        self.assertRaises(TypeError, Item.create, title=self.title, name=self.name, price=self.price,
                          category=self.category, earnings=-self.earnings, subscription_term='1', vat=self.tax)

        self.assertRaises(TypeError, Item.create, title=self.title, name=self.name, price=self.price,
                          category=self.category, earnings=-self.earnings, subscription_term='0', vat=self.tax)

        self.assertRaises(TypeError, Item.create, title=self.title, name=self.name, price=self.price,
                          category=self.category, earnings=-self.earnings, subscription_term='-1', vat=self.tax)

        self.assertRaises(TypeError, Item.create, title=self.title, name=self.name, price=self.price,
                          category=self.category, earnings=-self.earnings, subscription_term='1.1', vat=self.tax)

        self.assertRaises(TypeError, Item.create, title=self.title, name=self.name, price=self.price,
                          category=self.category, earnings=-self.earnings, subscription_term='-1.1', vat=self.tax)

        self.assertRaises(TypeError, Item.create, title=self.title, name=self.name, price=self.price,
                          category=self.category, earnings=-self.earnings, subscription_term='Text', vat=self.tax)

        self.assertRaises(TypeError, Item.create, title=self.title, name=self.name, price=self.price,
                          category=self.category, earnings=-self.earnings, subscription_term=1.1, vat=self.tax)

        self.assertRaises(TypeError, Item.create, title=self.title, name=self.name, price=self.price,
                          category=self.category, earnings=-self.earnings, subscription_term=-1.1, vat=self.tax)

        self.assertRaises(TypeError, Item.create, title=self.title, name=self.name, price=self.price,
                          category=self.category, earnings=-self.earnings, subscription_term=True, vat=self.tax)

        self.assertRaises(TypeError, Item.create, title=self.title, name=self.name, price=self.price,
                          category=self.category, earnings=-self.earnings, subscription_term=False, vat=self.tax)

        self.assertRaises(TypeError, Item.create, title=self.title, name=self.name, price=self.price,
                          category=self.category, earnings=-self.earnings, subscription_term=list(), vat=self.tax)

        self.assertRaises(TypeError, Item.create, title=self.title, name=self.name, price=self.price,
                          category=self.category, earnings=-self.earnings, subscription_term=tuple(), vat=self.tax)

        self.assertRaises(TypeError, Item.create, title=self.title, name=self.name, price=self.price,
                          category=self.category, earnings=-self.earnings, subscription_term=dict(), vat=self.tax)

        self.assertRaises(TypeError, Item.create, title=self.title, name=self.name, price=self.price,
                          category=self.category, earnings=-self.earnings, subscription_term=set(), vat=self.tax)

    def test_create_item_with_negative_int_or_0_as_subscription_term(self):
        self.assertRaises(TypeError, Item.create, title=self.title, name=self.name, price=self.price,
                          category=self.category, earnings=-self.earnings, subscription_term=0, vat=self.tax)

        self.assertRaises(TypeError, Item.create, title=self.title, name=self.name, price=self.price,
                          category=self.category, earnings=-self.earnings, subscription_term=-1, vat=self.tax)

    def test_create_item_with_not_Tax_as_vat(self):
        self.assertRaises(TypeError, Item.create, title=self.title, name=self.name, price=self.price,
                          category=self.category, earnings=-self.earnings, subscription_term=self.subscription_term,
                          vat='')

        self.assertRaises(TypeError, Item.create, title=self.title, name=self.name, price=self.price,
                          category=self.category, earnings=-self.earnings, subscription_term=self.subscription_term,
                          vat=' ')

        self.assertRaises(TypeError, Item.create, title=self.title, name=self.name, price=self.price,
                          category=self.category, earnings=-self.earnings, subscription_term=self.subscription_term,
                          vat='1')

        self.assertRaises(TypeError, Item.create, title=self.title, name=self.name, price=self.price,
                          category=self.category, earnings=-self.earnings, subscription_term=self.subscription_term,
                          vat='0')

        self.assertRaises(TypeError, Item.create, title=self.title, name=self.name, price=self.price,
                          category=self.category, earnings=-self.earnings, subscription_term=self.subscription_term,
                          vat='-1')

        self.assertRaises(TypeError, Item.create, title=self.title, name=self.name, price=self.price,
                          category=self.category, earnings=-self.earnings, subscription_term=self.subscription_term,
                          vat='1.1')

        self.assertRaises(TypeError, Item.create, title=self.title, name=self.name, price=self.price,
                          category=self.category, earnings=-self.earnings, subscription_term=self.subscription_term,
                          vat='-1.1')

        self.assertRaises(TypeError, Item.create, title=self.title, name=self.name, price=self.price,
                          category=self.category, earnings=-self.earnings, subscription_term=self.subscription_term,
                          vat='Text')

        self.assertRaises(TypeError, Item.create, title=self.title, name=self.name, price=self.price,
                          category=self.category, earnings=-self.earnings, subscription_term=self.subscription_term,
                          vat=1)

        self.assertRaises(TypeError, Item.create, title=self.title, name=self.name, price=self.price,
                          category=self.category, earnings=-self.earnings, subscription_term=self.subscription_term,
                          vat=0)

        self.assertRaises(TypeError, Item.create, title=self.title, name=self.name, price=self.price,
                          category=self.category, earnings=-self.earnings, subscription_term=self.subscription_term,
                          vat=-1)

        self.assertRaises(TypeError, Item.create, title=self.title, name=self.name, price=self.price,
                          category=self.category, earnings=-self.earnings, subscription_term=self.subscription_term,
                          vat=1.1)

        self.assertRaises(TypeError, Item.create, title=self.title, name=self.name, price=self.price,
                          category=self.category, earnings=-self.earnings, subscription_term=self.subscription_term,
                          vat=-1.1)

        self.assertRaises(TypeError, Item.create, title=self.title, name=self.name, price=self.price,
                          category=self.category, earnings=-self.earnings, subscription_term=self.subscription_term,
                          vat=True)

        self.assertRaises(TypeError, Item.create, title=self.title, name=self.name, price=self.price,
                          category=self.category, earnings=-self.earnings, subscription_term=self.subscription_term,
                          vat=False)

        self.assertRaises(TypeError, Item.create, title=self.title, name=self.name, price=self.price,
                          category=self.category, earnings=-self.earnings, subscription_term=self.subscription_term,
                          vat=None)

        self.assertRaises(TypeError, Item.create, title=self.title, name=self.name, price=self.price,
                          category=self.category, earnings=-self.earnings, subscription_term=self.subscription_term,
                          vat=list())

        self.assertRaises(TypeError, Item.create, title=self.title, name=self.name, price=self.price,
                          category=self.category, earnings=-self.earnings, subscription_term=self.subscription_term,
                          vat=tuple())

        self.assertRaises(TypeError, Item.create, title=self.title, name=self.name, price=self.price,
                          category=self.category, earnings=-self.earnings, subscription_term=self.subscription_term,
                          vat=dict())

        self.assertRaises(TypeError, Item.create, title=self.title, name=self.name, price=self.price,
                          category=self.category, earnings=-self.earnings, subscription_term=self.subscription_term,
                          vat=set())
