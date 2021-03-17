from django.test import TestCase
from .models import Address, Company, Customer, Tax, Item, SoldItem, Transaction, Marketplace, Receipt, Invoice, \
    AdvanceInvoice


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

