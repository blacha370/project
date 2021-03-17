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


class InvoiceTestCase(TestCase):
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

    def test_create_invoice(self):
        invoice = Invoice.create(receipt=self.receipt)
        self.assertIsInstance(invoice, Invoice)
        self.assertEqual(invoice.receipt, self.receipt)
        self.assertFalse(invoice.ended)
        self.assertIsNone(invoice.time)
        self.assertEqual(Invoice.objects.count(), 1)

    def test_create_multiple_invoices_with_same_receipt(self):
        invoice = Invoice.create(receipt=self.receipt)
        self.assertIsInstance(invoice, Invoice)
        self.assertEqual(invoice.receipt, self.receipt)
        self.assertFalse(invoice.ended)
        self.assertIsNone(invoice.time)
        self.assertEqual(Invoice.objects.count(), 1)

        self.assertRaises(TypeError, Invoice.create, receipt=self.receipt)
        self.assertEqual(Invoice.objects.count(), 1)

    def test_create_invoice_with_not_Receipt_as_receipt(self):
        self.assertRaises(TypeError, Invoice.create, receipt='')

        self.assertRaises(TypeError, Invoice.create, receipt=' ')

        self.assertRaises(TypeError, Invoice.create, receipt='1')

        self.assertRaises(TypeError, Invoice.create, receipt='0')

        self.assertRaises(TypeError, Invoice.create, receipt='-1')

        self.assertRaises(TypeError, Invoice.create, receipt='1.1')

        self.assertRaises(TypeError, Invoice.create, receipt='-1.1')

        self.assertRaises(TypeError, Invoice.create, receipt='Text')

        self.assertRaises(TypeError, Invoice.create, receipt=1)

        self.assertRaises(TypeError, Invoice.create, receipt=0)

        self.assertRaises(TypeError, Invoice.create, receipt=-1)

        self.assertRaises(TypeError, Invoice.create, receipt=1.1)

        self.assertRaises(TypeError, Invoice.create, receipt=-1.1)

        self.assertRaises(TypeError, Invoice.create, receipt=True)

        self.assertRaises(TypeError, Invoice.create, receipt=False)

        self.assertRaises(TypeError, Invoice.create, receipt=None)

        self.assertRaises(TypeError, Invoice.create, receipt=list())

        self.assertRaises(TypeError, Invoice.create, receipt=tuple())

        self.assertRaises(TypeError, Invoice.create, receipt=dict())

        self.assertRaises(TypeError, Invoice.create, receipt=set())
        self.assertEqual(Invoice.objects.count(), 0)


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
