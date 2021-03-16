from django.test import TestCase
from .models import Address, Company, Customer, Tax


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


class CompanyTestCase(TestCase):
    def setUp(self):
        self.address = Address.create(country='Poland', city='Warsaw', postal_code='10-100', street='Street',
                                      building_number=3, apartment_number=5)
        self.name = 'Company'

    def test_create_company(self):
        company = Company.create(name=self.name, address=self.address)
        self.assertIsInstance(company, Company)
        self.assertEqual(company.name, self.name)
        self.assertEqual(company.address, self.address)
        self.assertIsInstance(company.SKU, str)
        self.assertEqual(len(company.SKU), 150)
        self.assertEqual(Company.objects.count(), 1)

    def test_create_company_with_same_name(self):
        company = Company.create(name=self.name, address=self.address)
        self.assertIsInstance(company, Company)
        self.assertEqual(company.name, self.name)
        self.assertEqual(company.address, self.address)
        self.assertIsInstance(company.SKU, str)
        self.assertEqual(len(company.SKU), 150)
        self.assertEqual(Company.objects.count(), 1)

        address = Address.create(country='Poland', city='Warsaw', postal_code='10-100', street='Street',
                                 building_number=3, apartment_number=5)
        self.assertRaises(TypeError, Company.create, name=self.name, address=address)
        self.assertEqual(Company.objects.count(), 1)

    def test_create_company_with_too_long_name(self):
        name = '1' * 101
        self.assertRaises(TypeError, Company.create, name=name, address=self.address)

    def test_create_company_with_same_address(self):
        company = Company.create(name=self.name, address=self.address)
        self.assertIsInstance(company, Company)
        self.assertEqual(company.name, self.name)
        self.assertEqual(company.address, self.address)
        self.assertIsInstance(company.SKU, str)
        self.assertEqual(len(company.SKU), 150)
        self.assertEqual(Company.objects.count(), 1)

        self.assertRaises(TypeError, Company.create, name='Second company', address=self.address)
        self.assertEqual(Company.objects.count(), 1)

    def test_create_company_with_not_string_as_name(self):
        self.assertRaises(TypeError, Company.create, name=1, address=self.address)

        self.assertRaises(TypeError, Company.create, name=0, address=self.address)

        self.assertRaises(TypeError, Company.create, name=-1, address=self.address)

        self.assertRaises(TypeError, Company.create, name=1.1, address=self.address)

        self.assertRaises(TypeError, Company.create, name=-1.1, address=self.address)

        self.assertRaises(TypeError, Company.create, name=True, address=self.address)

        self.assertRaises(TypeError, Company.create, name=False, address=self.address)

        self.assertRaises(TypeError, Company.create, name=None, address=self.address)

        self.assertRaises(TypeError, Company.create, name=list(), address=self.address)

        self.assertRaises(TypeError, Company.create, name=tuple(), address=self.address)

        self.assertRaises(TypeError, Company.create, name=dict(), address=self.address)

        self.assertRaises(TypeError, Company.create, name=set(), address=self.address)
        self.assertEqual(Company.objects.count(), 0)

    def test_create_company_with_empty_string_as_name(self):
        self.assertRaises(TypeError, Company.create, name='', address=self.address)

        self.assertRaises(TypeError, Company.create, name=' ', address=self.address)
        self.assertEqual(Company.objects.count(), 0)

    def test_create_company_with_not_Address_as_address(self):
        self.assertRaises(TypeError, Company.create, name=self.name, address='')

        self.assertRaises(TypeError, Company.create, name=self.name, address=' ')

        self.assertRaises(TypeError, Company.create, name=self.name, address='Text')

        self.assertRaises(TypeError, Company.create, name=self.name, address='1')

        self.assertRaises(TypeError, Company.create, name=self.name, address='0')

        self.assertRaises(TypeError, Company.create, name=self.name, address='-1')

        self.assertRaises(TypeError, Company.create, name=self.name, address=1)

        self.assertRaises(TypeError, Company.create, name=self.name, address=0)

        self.assertRaises(TypeError, Company.create, name=self.name, address=-1)

        self.assertRaises(TypeError, Company.create, name=self.name, address=1.1)

        self.assertRaises(TypeError, Company.create, name=self.name, address=-1.1)

        self.assertRaises(TypeError, Company.create, name=self.name, address=True)

        self.assertRaises(TypeError, Company.create, name=self.name, address=False)

        self.assertRaises(TypeError, Company.create, name=self.name, address=None)

        self.assertRaises(TypeError, Company.create, name=self.name, address=list())

        self.assertRaises(TypeError, Company.create, name=self.name, address=tuple())

        self.assertRaises(TypeError, Company.create, name=self.name, address=dict())

        self.assertRaises(TypeError, Company.create, name=self.name, address=set())
        self.assertEqual(Company.objects.count(), 0)


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


class TaxTestCase(TestCase):
    def test_create_tax(self):
        tax = Tax.create(tax_value=0.23)
        self.assertIsInstance(tax, Tax)
        self.assertEqual(tax.tax_value, 0.23)
        self.assertEqual(tax.tax_name, 'Vat_0.23')
        self.assertEqual(Tax.objects.count(), 1)

    def test_create_tax_with_not_float_as_tax_value(self):
        self.assertRaises(TypeError, Tax.create, tax_value='')

        self.assertRaises(TypeError, Tax.create, tax_value=' ')

        self.assertRaises(TypeError, Tax.create, tax_value='Text')

        self.assertRaises(TypeError, Tax.create, tax_value='1')

        self.assertRaises(TypeError, Tax.create, tax_value='0')

        self.assertRaises(TypeError, Tax.create, tax_value='-1')

        self.assertRaises(TypeError, Tax.create, tax_value='0.23')

        self.assertRaises(TypeError, Tax.create, tax_value=1)

        self.assertRaises(TypeError, Tax.create, tax_value=0)

        self.assertRaises(TypeError, Tax.create, tax_value=-1)

        self.assertRaises(TypeError, Tax.create, tax_value=True)

        self.assertRaises(TypeError, Tax.create, tax_value=False)

        self.assertRaises(TypeError, Tax.create, tax_value=None)

        self.assertRaises(TypeError, Tax.create, tax_value=list())

        self.assertRaises(TypeError, Tax.create, tax_value=tuple())

        self.assertRaises(TypeError, Tax.create, tax_value=dict())

        self.assertRaises(TypeError, Tax.create, tax_value=set())
        self.assertEqual(Tax.objects.count(), 0)

    def test_create_tax_with_wrong_float_value(self):
        self.assertRaises(TypeError, Tax.create, tax_value=1.23)

        self.assertRaises(TypeError, Tax.create, tax_value=-1.23)

        self.assertRaises(TypeError, Tax.create, tax_value=-0.23)
        self.assertEqual(Tax.objects.count(), 0)
