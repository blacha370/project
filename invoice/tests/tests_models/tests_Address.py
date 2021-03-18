from django.test import TestCase
from ...models import *


class AddressTestCase(TestCase):
    def setUp(self):
        self.country = 'Poland'
        self.city = 'Warsaw'
        self.postal_code = '10-100'
        self.street = 'Street'
        self.building_number = 3
        self.apartment_number = 5

    def test_create_address_with_correct_data(self):
        address = Address.create(country=self.country, city=self.city, postal_code=self.postal_code, street=self.street,
                                 building_number=self.building_number, apartment_number=self.apartment_number)
        self.assertIsInstance(address, Address)
        self.assertEqual(address.country, self.country)
        self.assertEqual(address.city, self.city)
        self.assertEqual(address.postal_code, self.postal_code)
        self.assertEqual(address.street, self.street)
        self.assertEqual(address.building_number, self.building_number)
        self.assertEqual(address.apartment_number, self.apartment_number)
        self.assertEqual(Address.objects.count(), 1)

        address = Address.create(country=self.country, city=self.city, postal_code=self.postal_code, street=self.street,
                                 building_number=self.building_number)
        self.assertIsInstance(address, Address)
        self.assertEqual(address.country, self.country)
        self.assertEqual(address.city, self.city)
        self.assertEqual(address.postal_code, self.postal_code)
        self.assertEqual(address.street, self.street)
        self.assertEqual(address.building_number, self.building_number)
        self.assertEqual(address.apartment_number, None)
        self.assertEqual(Address.objects.count(), 2)

    def test_create_address_with_not_string_as_country(self):
        self.assertRaises(TypeError, Address.create, country=1, city=self.city, postal_code=self.postal_code,
                          street=self.street, building_number=self.building_number,
                          apartment_number=self.apartment_number)

        self.assertRaises(TypeError, Address.create, country=0, city=self.city, postal_code=self.postal_code,
                          street=self.street, building_number=self.building_number,
                          apartment_number=self.apartment_number)

        self.assertRaises(TypeError, Address.create, country=-1, city=self.city, postal_code=self.postal_code,
                          street=self.street, building_number=self.building_number,
                          apartment_number=self.apartment_number)

        self.assertRaises(TypeError, Address.create, country=1.1, city=self.city, postal_code=self.postal_code,
                          street=self.street, building_number=self.building_number,
                          apartment_number=self.apartment_number)

        self.assertRaises(TypeError, Address.create, country=-1.1, city=self.city, postal_code=self.postal_code,
                          street=self.street, building_number=self.building_number,
                          apartment_number=self.apartment_number)

        self.assertRaises(TypeError, Address.create, country=True, city=self.city, postal_code=self.postal_code,
                          street=self.street, building_number=self.building_number,
                          apartment_number=self.apartment_number)

        self.assertRaises(TypeError, Address.create, country=False, city=self.city, postal_code=self.postal_code,
                          street=self.street, building_number=self.building_number,
                          apartment_number=self.apartment_number)

        self.assertRaises(TypeError, Address.create, country=None, city=self.city, postal_code=self.postal_code,
                          street=self.street, building_number=self.building_number,
                          apartment_number=self.apartment_number)

        self.assertRaises(TypeError, Address.create, country=list(), city=self.city, postal_code=self.postal_code,
                          street=self.street, building_number=self.building_number,
                          apartment_number=self.apartment_number)

        self.assertRaises(TypeError, Address.create, country=tuple(), city=self.city, postal_code=self.postal_code,
                          street=self.street, building_number=self.building_number,
                          apartment_number=self.apartment_number)

        self.assertRaises(TypeError, Address.create, country=dict(), city=self.city, postal_code=self.postal_code,
                          street=self.street, building_number=self.building_number,
                          apartment_number=self.apartment_number)

        self.assertRaises(TypeError, Address.create, country=set(), city=self.city, postal_code=self.postal_code,
                          street=self.street, building_number=self.building_number,
                          apartment_number=self.apartment_number)
        self.assertEqual(Address.objects.count(), 0)

    def test_create_address_with_empty_string_as_country(self):
        self.assertRaises(TypeError, Address.create, country='', city=self.city, postal_code=self.postal_code,
                          street=self.street, building_number=self.building_number,
                          apartment_number=self.apartment_number)

        self.assertRaises(TypeError, Address.create, country=' ', city=self.city, postal_code=self.postal_code,
                          street=self.street, building_number=self.building_number,
                          apartment_number=self.apartment_number)
        self.assertEqual(Address.objects.count(), 0)

    def test_create_address_with_too_long_string_as_country(self):
        country = '1' * 51
        self.assertRaises(TypeError, Address.create, country=country, city=self.city, postal_code=self.postal_code,
                          street=self.street, building_number=self.building_number,
                          apartment_number=self.apartment_number)
        self.assertEqual(Address.objects.count(), 0)

    def test_create_address_with_not_string_as_city(self):
        self.assertRaises(TypeError, Address.create, country=self.country, city=1, postal_code=self.postal_code,
                          street=self.street, building_number=self.building_number,
                          apartment_number=self.apartment_number)

        self.assertRaises(TypeError, Address.create, country=self.country, city=0, postal_code=self.postal_code,
                          street=self.street, building_number=self.building_number,
                          apartment_number=self.apartment_number)

        self.assertRaises(TypeError, Address.create, country=self.country, city=-1, postal_code=self.postal_code,
                          street=self.street, building_number=self.building_number,
                          apartment_number=self.apartment_number)

        self.assertRaises(TypeError, Address.create, country=self.country, city=1.1, postal_code=self.postal_code,
                          street=self.street, building_number=self.building_number,
                          apartment_number=self.apartment_number)

        self.assertRaises(TypeError, Address.create, country=self.country, city=-1.1, postal_code=self.postal_code,
                          street=self.street, building_number=self.building_number,
                          apartment_number=self.apartment_number)

        self.assertRaises(TypeError, Address.create, country=self.country, city=True, postal_code=self.postal_code,
                          street=self.street, building_number=self.building_number,
                          apartment_number=self.apartment_number)

        self.assertRaises(TypeError, Address.create, country=self.country, city=False, postal_code=self.postal_code,
                          street=self.street, building_number=self.building_number,
                          apartment_number=self.apartment_number)

        self.assertRaises(TypeError, Address.create, country=self.country, city=None, postal_code=self.postal_code,
                          street=self.street, building_number=self.building_number,
                          apartment_number=self.apartment_number)

        self.assertRaises(TypeError, Address.create, country=self.country, city=list(), postal_code=self.postal_code,
                          street=self.street, building_number=self.building_number,
                          apartment_number=self.apartment_number)

        self.assertRaises(TypeError, Address.create, country=self.country, city=tuple(), postal_code=self.postal_code,
                          street=self.street, building_number=self.building_number,
                          apartment_number=self.apartment_number)

        self.assertRaises(TypeError, Address.create, country=self.country, city=dict(), postal_code=self.postal_code,
                          street=self.street, building_number=self.building_number,
                          apartment_number=self.apartment_number)

        self.assertRaises(TypeError, Address.create, country=self.country, city=set(), postal_code=self.postal_code,
                          street=self.street, building_number=self.building_number,
                          apartment_number=self.apartment_number)
        self.assertEqual(Address.objects.count(), 0)

    def test_create_address_with_empty_string_as_city(self):
        self.assertRaises(TypeError, Address.create, country=self.country, city='', postal_code=self.postal_code,
                          street=self.street, building_number=self.building_number,
                          apartment_number=self.apartment_number)

        self.assertRaises(TypeError, Address.create, country=self.country, city=' ', postal_code=self.postal_code,
                          street=self.street, building_number=self.building_number,
                          apartment_number=self.apartment_number)
        self.assertEqual(Address.objects.count(), 0)

    def test_create_address_with_too_long_string_as_city(self):
        city = '1' * 101
        self.assertRaises(TypeError, Address.create, country=self.country, city=city, postal_code=self.postal_code,
                          street=self.street, building_number=self.building_number,
                          apartment_number=self.apartment_number)
        self.assertEqual(Address.objects.count(), 0)

    def test_create_address_with_not_string_as_postal_code(self):
        self.assertRaises(TypeError, Address.create, country=self.country, city=self.city, postal_code=1,
                          street=self.street, building_number=self.building_number,
                          apartment_number=self.apartment_number)

        self.assertRaises(TypeError, Address.create, country=self.country, city=self.city, postal_code=0,
                          street=self.street, building_number=self.building_number,
                          apartment_number=self.apartment_number)

        self.assertRaises(TypeError, Address.create, country=self.country, city=self.city, postal_code=-1,
                          street=self.street, building_number=self.building_number,
                          apartment_number=self.apartment_number)

        self.assertRaises(TypeError, Address.create, country=self.country, city=self.city, postal_code=1.1,
                          street=self.street, building_number=self.building_number,
                          apartment_number=self.apartment_number)

        self.assertRaises(TypeError, Address.create, country=self.country, city=self.city, postal_code=-1.1,
                          street=self.street, building_number=self.building_number,
                          apartment_number=self.apartment_number)

        self.assertRaises(TypeError, Address.create, country=self.country, city=self.city, postal_code=True,
                          street=self.street, building_number=self.building_number,
                          apartment_number=self.apartment_number)

        self.assertRaises(TypeError, Address.create, country=self.country, city=self.city, postal_code=False,
                          street=self.street, building_number=self.building_number,
                          apartment_number=self.apartment_number)

        self.assertRaises(TypeError, Address.create, country=self.country, city=self.city, postal_code=None,
                          street=self.street, building_number=self.building_number,
                          apartment_number=self.apartment_number)

        self.assertRaises(TypeError, Address.create, country=self.country, city=self.city, postal_code=list(),
                          street=self.street, building_number=self.building_number,
                          apartment_number=self.apartment_number)

        self.assertRaises(TypeError, Address.create, country=self.country, city=self.city, postal_code=tuple(),
                          street=self.street, building_number=self.building_number,
                          apartment_number=self.apartment_number)

        self.assertRaises(TypeError, Address.create, country=self.country, city=self.city, postal_code=dict(),
                          street=self.street, building_number=self.building_number,
                          apartment_number=self.apartment_number)

        self.assertRaises(TypeError, Address.create, country=self.country, city=self.city, postal_code=set(),
                          street=self.street, building_number=self.building_number,
                          apartment_number=self.apartment_number)
        self.assertEqual(Address.objects.count(), 0)

    def test_create_address_with_empty_string_as_postal_code(self):
        self.assertRaises(TypeError, Address.create, country=self.country, city=self.city, postal_code='',
                          street=self.street, building_number=self.building_number,
                          apartment_number=self.apartment_number)

        self.assertRaises(TypeError, Address.create, country=self.country, city=self.city, postal_code=' ',
                          street=self.street, building_number=self.building_number,
                          apartment_number=self.apartment_number)
        self.assertEqual(Address.objects.count(), 0)

    def test_create_address_with_too_long_string_as_postal_code(self):
        postal_code = '1' * 7
        self.assertRaises(TypeError, Address.create, country=self.country, city=self.city, postal_code=postal_code,
                          street=self.street, building_number=self.building_number,
                          apartment_number=self.apartment_number)
        self.assertEqual(Address.objects.count(), 0)

    def test_create_address_with_not_string_as_street(self):
        self.assertRaises(TypeError, Address.create, country=self.country, city=self.city, postal_code=self.postal_code,
                          street=1, building_number=self.building_number, apartment_number=self.apartment_number)

        self.assertRaises(TypeError, Address.create, country=self.country, city=self.city, postal_code=self.postal_code,
                          street=0, building_number=self.building_number, apartment_number=self.apartment_number)

        self.assertRaises(TypeError, Address.create, country=self.country, city=self.city, postal_code=self.postal_code,
                          street=-1, building_number=self.building_number, apartment_number=self.apartment_number)

        self.assertRaises(TypeError, Address.create, country=self.country, city=self.city, postal_code=self.postal_code,
                          street=1.1, building_number=self.building_number, apartment_number=self.apartment_number)

        self.assertRaises(TypeError, Address.create, country=self.country, city=self.city, postal_code=self.postal_code,
                          street=-1.1, building_number=self.building_number, apartment_number=self.apartment_number)

        self.assertRaises(TypeError, Address.create, country=self.country, city=self.city, postal_code=self.postal_code,
                          street=True, building_number=self.building_number, apartment_number=self.apartment_number)

        self.assertRaises(TypeError, Address.create, country=self.country, city=self.city, postal_code=self.postal_code,
                          street=False, building_number=self.building_number, apartment_number=self.apartment_number)

        self.assertRaises(TypeError, Address.create, country=self.country, city=self.city, postal_code=self.postal_code,
                          street=None, building_number=self.building_number, apartment_number=self.apartment_number)

        self.assertRaises(TypeError, Address.create, country=self.country, city=self.city, postal_code=self.postal_code,
                          street=list(), building_number=self.building_number, apartment_number=self.apartment_number)

        self.assertRaises(TypeError, Address.create, country=self.country, city=self.city, postal_code=self.postal_code,
                          street=tuple(), building_number=self.building_number, apartment_number=self.apartment_number)

        self.assertRaises(TypeError, Address.create, country=self.country, city=self.city, postal_code=self.postal_code,
                          street=dict(), building_number=self.building_number, apartment_number=self.apartment_number)

        self.assertRaises(TypeError, Address.create, country=self.country, city=self.city, postal_code=self.postal_code,
                          street=set(), building_number=self.building_number, apartment_number=self.apartment_number)
        self.assertEqual(Address.objects.count(), 0)

    def test_create_address_with_empty_string_as_street(self):
        self.assertRaises(TypeError, Address.create, country=self.country, city=self.city, postal_code=self.postal_code,
                          street='', building_number=self.building_number, apartment_number=self.apartment_number)

        self.assertRaises(TypeError, Address.create, country=self.country, city=self.city, postal_code=self.postal_code,
                          street=' ', building_number=self.building_number, apartment_number=self.apartment_number)
        self.assertEqual(Address.objects.count(), 0)

    def test_create_address_with_too_long_string_as_street(self):
        street = '1' * 101
        self.assertRaises(TypeError, Address.create, country=self.country, city=self.city, postal_code=self.postal_code,
                          street=street, building_number=self.building_number, apartment_number=self.apartment_number)
        self.assertEqual(Address.objects.count(), 0)

    def test_create_address_with_not_int_as_building_number(self):
        self.assertRaises(TypeError, Address.create, country=self.country, city=self.city, postal_code=self.postal_code,
                          street=self.street, building_number='', apartment_number=self.apartment_number)

        self.assertRaises(TypeError, Address.create, country=self.country, city=self.city, postal_code=self.postal_code,
                          street=self.street, building_number=' ', apartment_number=self.apartment_number)

        self.assertRaises(TypeError, Address.create, country=self.country, city=self.city, postal_code=self.postal_code,
                          street=self.street, building_number='Text', apartment_number=self.apartment_number)

        self.assertRaises(TypeError, Address.create, country=self.country, city=self.city, postal_code=self.postal_code,
                          street=self.street, building_number='1', apartment_number=self.apartment_number)

        self.assertRaises(TypeError, Address.create, country=self.country, city=self.city, postal_code=self.postal_code,
                          street=self.street, building_number='0', apartment_number=self.apartment_number)

        self.assertRaises(TypeError, Address.create, country=self.country, city=self.city, postal_code=self.postal_code,
                          street=self.street, building_number='-1', apartment_number=self.apartment_number)

        self.assertRaises(TypeError, Address.create, country=self.country, city=self.city, postal_code=self.postal_code,
                          street=self.street, building_number=1.1, apartment_number=self.apartment_number)

        self.assertRaises(TypeError, Address.create, country=self.country, city=self.city, postal_code=self.postal_code,
                          street=self.street, building_number=-1.1, apartment_number=self.apartment_number)

        self.assertRaises(TypeError, Address.create, country=self.country, city=self.city, postal_code=self.postal_code,
                          street=self.street, building_number=True, apartment_number=self.apartment_number)

        self.assertRaises(TypeError, Address.create, country=self.country, city=self.city, postal_code=self.postal_code,
                          street=self.street, building_number=False, apartment_number=self.apartment_number)

        self.assertRaises(TypeError, Address.create, country=self.country, city=self.city, postal_code=self.postal_code,
                          street=self.street, building_number=None, apartment_number=self.apartment_number)

        self.assertRaises(TypeError, Address.create, country=self.country, city=self.city, postal_code=self.postal_code,
                          street=self.street, building_number=list(), apartment_number=self.apartment_number)

        self.assertRaises(TypeError, Address.create, country=self.country, city=self.city, postal_code=self.postal_code,
                          street=self.street, building_number=tuple(), apartment_number=self.apartment_number)

        self.assertRaises(TypeError, Address.create, country=self.country, city=self.city, postal_code=self.postal_code,
                          street=self.street, building_number=dict(), apartment_number=self.apartment_number)

        self.assertRaises(TypeError, Address.create, country=self.country, city=self.city, postal_code=self.postal_code,
                          street=self.street, building_number=set(), apartment_number=self.apartment_number)
        self.assertEqual(Address.objects.count(), 0)

    def test_create_address_with_negative_int_and_0_as_building_number(self):
        self.assertRaises(TypeError, Address.create, country=self.country, city=self.city, postal_code=self.postal_code,
                          street=self.street, building_number=-1, apartment_number=self.apartment_number)

        self.assertRaises(TypeError, Address.create, country=self.country, city=self.city, postal_code=self.postal_code,
                          street=self.street, building_number=0, apartment_number=self.apartment_number)
        self.assertEqual(Address.objects.count(), 0)

    def test_create_address_with_not_int_as_apartment_number(self):
        self.assertRaises(TypeError, Address.create, country=self.country, city=self.city, postal_code=self.postal_code,
                          street=self.street, building_number=self.building_number, apartment_number='')

        self.assertRaises(TypeError, Address.create, country=self.country, city=self.city, postal_code=self.postal_code,
                          street=self.street, building_number=self.building_number, apartment_number=' ')

        self.assertRaises(TypeError, Address.create, country=self.country, city=self.city, postal_code=self.postal_code,
                          street=self.street, building_number=self.building_number, apartment_number='Text')

        self.assertRaises(TypeError, Address.create, country=self.country, city=self.city, postal_code=self.postal_code,
                          street=self.street, building_number=self.building_number, apartment_number='1')

        self.assertRaises(TypeError, Address.create, country=self.country, city=self.city, postal_code=self.postal_code,
                          street=self.street, building_number=self.building_number, apartment_number='0')

        self.assertRaises(TypeError, Address.create, country=self.country, city=self.city, postal_code=self.postal_code,
                          street=self.street, building_number=self.building_number, apartment_number='-1')

        self.assertRaises(TypeError, Address.create, country=self.country, city=self.city, postal_code=self.postal_code,
                          street=self.street, building_number=self.building_number, apartment_number=1.1)

        self.assertRaises(TypeError, Address.create, country=self.country, city=self.city, postal_code=self.postal_code,
                          street=self.street, building_number=self.building_number, apartment_number=-1.1)

        self.assertRaises(TypeError, Address.create, country=self.country, city=self.city, postal_code=self.postal_code,
                          street=self.street, building_number=self.building_number, apartment_number=True)

        self.assertRaises(TypeError, Address.create, country=self.country, city=self.city, postal_code=self.postal_code,
                          street=self.street, building_number=self.building_number, apartment_number=False)

        self.assertRaises(TypeError, Address.create, country=self.country, city=self.city, postal_code=self.postal_code,
                          street=self.street, building_number=self.building_number, apartment_number=list())

        self.assertRaises(TypeError, Address.create, country=self.country, city=self.city, postal_code=self.postal_code,
                          street=self.street, building_number=self.building_number, apartment_number=tuple())

        self.assertRaises(TypeError, Address.create, country=self.country, city=self.city, postal_code=self.postal_code,
                          street=self.street, building_number=self.building_number, apartment_number=dict())

        self.assertRaises(TypeError, Address.create, country=self.country, city=self.city, postal_code=self.postal_code,
                          street=self.street, building_number=self.building_number, apartment_number=set())
        self.assertEqual(Address.objects.count(), 0)

    def test_create_address_with_negative_int_and_0_as_apartment_number(self):
        self.assertRaises(TypeError, Address.create, country=self.country, city=self.city, postal_code=self.postal_code,
                          street=self.street, building_number=self.building_number, apartment_number=-1)

        self.assertRaises(TypeError, Address.create, country=self.country, city=self.city, postal_code=self.postal_code,
                          street=self.street, building_number=self.building_number, apartment_number=0)
        self.assertEqual(Address.objects.count(), 0)

    def test_str_method(self):
        address = Address.create(country=self.country, city=self.city, postal_code=self.postal_code, street=self.street,
                                 building_number=self.building_number, apartment_number=self.apartment_number)
        self.assertIn(self.country, str(address))
        self.assertIn(self.city, str(address))
        self.assertIn(self.postal_code, str(address))
        self.assertIn(self.street, str(address))
        self.assertIn(str(self.building_number), str(address))
        self.assertIn(str(self.apartment_number), str(address))
