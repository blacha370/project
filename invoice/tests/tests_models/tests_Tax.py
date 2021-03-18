from django.test import TestCase
from ...models import Tax


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
