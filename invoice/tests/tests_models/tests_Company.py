from django.test import TestCase
from ...models import Address, Company


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
