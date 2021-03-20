from django.test import TestCase
from ...models import Address, Customer


class CustomerTestCase(TestCase):
    def setUp(self):
        self.address = Address.create(country='Poland', city='Warsaw', postal_code='10-100', street='Street',
                                      building_number=3, apartment_number=5)
        self.name = 'Customer'

    def test_create_customer(self):
        customer = Customer.create(name=self.name, address=self.address)
        self.assertIsInstance(customer, Customer)
        self.assertEqual(customer.name, self.name)
        self.assertEqual(customer.address, self.address)
        self.assertEqual(Customer.objects.count(), 1)

    def test_create_customer_with_not_string_as_name(self):
        self.assertRaises(TypeError, Customer.create, name=1, address=self.address)

        self.assertRaises(TypeError, Customer.create, name=0, address=self.address)

        self.assertRaises(TypeError, Customer.create, name=-1, address=self.address)

        self.assertRaises(TypeError, Customer.create, name=1.1, address=self.address)

        self.assertRaises(TypeError, Customer.create, name=-1.1, address=self.address)

        self.assertRaises(TypeError, Customer.create, name=True, address=self.address)

        self.assertRaises(TypeError, Customer.create, name=False, address=self.address)

        self.assertRaises(TypeError, Customer.create, name=None, address=self.address)

        self.assertRaises(TypeError, Customer.create, name=list(), address=self.address)

        self.assertRaises(TypeError, Customer.create, name=tuple(), address=self.address)

        self.assertRaises(TypeError, Customer.create, name=dict(), address=self.address)

        self.assertRaises(TypeError, Customer.create, name=set(), address=self.address)
        self.assertEqual(Customer.objects.count(), 0)

    def test_create_customer_with_empty_string_as_name(self):
        self.assertRaises(TypeError, Customer.create, name='', address=self.address)

        self.assertRaises(TypeError, Customer.create, name=' ', address=self.address)
        self.assertEqual(Customer.objects.count(), 0)

    def test_create_customer_with_too_long_name(self):
        name = '1' * 101
        self.assertRaises(TypeError, Customer.create, name=name, address=self.address)
        self.assertEqual(Customer.objects.count(), 0)

    def test_create_customer_with_not_Address_as_address(self):
        self.assertRaises(TypeError, Customer.create, name=self.name, address='')

        self.assertRaises(TypeError, Customer.create, name=self.name, address=' ')

        self.assertRaises(TypeError, Customer.create, name=self.name, address='Text')

        self.assertRaises(TypeError, Customer.create, name=self.name, address='1')

        self.assertRaises(TypeError, Customer.create, name=self.name, address='0')

        self.assertRaises(TypeError, Customer.create, name=self.name, address='-1')

        self.assertRaises(TypeError, Customer.create, name=self.name, address=1)

        self.assertRaises(TypeError, Customer.create, name=self.name, address=0)

        self.assertRaises(TypeError, Customer.create, name=self.name, address=-1)

        self.assertRaises(TypeError, Customer.create, name=self.name, address=1.1)

        self.assertRaises(TypeError, Customer.create, name=self.name, address=-1.1)

        self.assertRaises(TypeError, Customer.create, name=self.name, address=True)

        self.assertRaises(TypeError, Customer.create, name=self.name, address=False)

        self.assertRaises(TypeError, Customer.create, name=self.name, address=None)

        self.assertRaises(TypeError, Customer.create, name=self.name, address=list())

        self.assertRaises(TypeError, Customer.create, name=self.name, address=tuple())

        self.assertRaises(TypeError, Customer.create, name=self.name, address=dict())

        self.assertRaises(TypeError, Customer.create, name=self.name, address=set())
