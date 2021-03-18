from rest_framework.test import APITestCase, APIRequestFactory
from ...views import CreateTax, Tax


class CreateTaxTestCase(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = CreateTax.as_view()

    def test_create_tax(self):
        request = self.factory.post('create_tax', {'tax_value': 0.12}, format='json')
        response = self.view(request)
        tax = Tax.objects.get(pk=1)
        self.assertEqual(Tax.objects.count(), 1)
        self.assertEqual(response.data['status'], 'OK')
        self.assertEqual(response.data['tax']['tax_name'], tax.tax_name)
        self.assertEqual(response.data['tax']['tax_value'], tax.tax_value)
        self.assertEqual(response.data['tax']['tax_name'], 'Vat_0.12')
        self.assertEqual(response.data['tax']['tax_value'], 0.12)

    def test_create_multiple_taxes_with_same_value(self):
        request = self.factory.post('create_tax', {'tax_value': 0.12}, format='json')
        response = self.view(request)
        tax = Tax.objects.get(pk=1)
        self.assertEqual(Tax.objects.count(), 1)
        self.assertEqual(response.data['status'], 'OK')
        self.assertEqual(response.data['tax']['tax_name'], tax.tax_name)
        self.assertEqual(response.data['tax']['tax_value'], tax.tax_value)
        self.assertEqual(response.data['tax']['tax_name'], 'Vat_0.12')
        self.assertEqual(response.data['tax']['tax_value'], 0.12)

        request = self.factory.post('create_tax', {'tax_value': 0.12}, format='json')
        response = self.view(request)
        self.assertEqual(Tax.objects.count(), 1)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Tax value error: tax with this value exist')

    def test_create_tax_with_not_float_as_value(self):
        request = self.factory.post('create_tax', {'tax_value': ''}, format='json')
        response = self.view(request)
        self.assertEqual(Tax.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'],
                         'Tax value error: tax_value should be float greater on equal to 0 and lower than 1')

        request = self.factory.post('create_tax', {'tax_value': ' '}, format='json')
        response = self.view(request)
        self.assertEqual(Tax.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'],
                         'Tax value error: tax_value should be float greater on equal to 0 and lower than 1')

        request = self.factory.post('create_tax', {'tax_value': '1'}, format='json')
        response = self.view(request)
        self.assertEqual(Tax.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'],
                         'Tax value error: tax_value should be float greater on equal to 0 and lower than 1')

        request = self.factory.post('create_tax', {'tax_value': '0'}, format='json')
        response = self.view(request)
        self.assertEqual(Tax.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'],
                         'Tax value error: tax_value should be float greater on equal to 0 and lower than 1')

        request = self.factory.post('create_tax', {'tax_value': '-1'}, format='json')
        response = self.view(request)
        self.assertEqual(Tax.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'],
                         'Tax value error: tax_value should be float greater on equal to 0 and lower than 1')

        request = self.factory.post('create_tax', {'tax_value': '0.1'}, format='json')
        response = self.view(request)
        self.assertEqual(Tax.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'],
                         'Tax value error: tax_value should be float greater on equal to 0 and lower than 1')

        request = self.factory.post('create_tax', {'tax_value': '-0.1'}, format='json')
        response = self.view(request)
        self.assertEqual(Tax.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'],
                         'Tax value error: tax_value should be float greater on equal to 0 and lower than 1')

        request = self.factory.post('create_tax', {'tax_value': 'Text'}, format='json')
        response = self.view(request)
        self.assertEqual(Tax.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'],
                         'Tax value error: tax_value should be float greater on equal to 0 and lower than 1')

        request = self.factory.post('create_tax', {'tax_value': 1}, format='json')
        response = self.view(request)
        self.assertEqual(Tax.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'],
                         'Tax value error: tax_value should be float greater on equal to 0 and lower than 1')

        request = self.factory.post('create_tax', {'tax_value': 0}, format='json')
        response = self.view(request)
        self.assertEqual(Tax.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'],
                         'Tax value error: tax_value should be float greater on equal to 0 and lower than 1')

        request = self.factory.post('create_tax', {'tax_value': -1}, format='json')
        response = self.view(request)
        self.assertEqual(Tax.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'],
                         'Tax value error: tax_value should be float greater on equal to 0 and lower than 1')

        request = self.factory.post('create_tax', {'tax_value': True}, format='json')
        response = self.view(request)
        self.assertEqual(Tax.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'],
                         'Tax value error: tax_value should be float greater on equal to 0 and lower than 1')

        request = self.factory.post('create_tax', {'tax_value': False}, format='json')
        response = self.view(request)
        self.assertEqual(Tax.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'],
                         'Tax value error: tax_value should be float greater on equal to 0 and lower than 1')

        request = self.factory.post('create_tax', {'tax_value': list()}, format='json')
        response = self.view(request)
        self.assertEqual(Tax.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'],
                         'Tax value error: tax_value should be float greater on equal to 0 and lower than 1')

        request = self.factory.post('create_tax', {'tax_value': tuple()}, format='json')
        response = self.view(request)
        self.assertEqual(Tax.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'],
                         'Tax value error: tax_value should be float greater on equal to 0 and lower than 1')

        request = self.factory.post('create_tax', {'tax_value': dict()}, format='json')
        response = self.view(request)
        self.assertEqual(Tax.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'],
                         'Tax value error: tax_value should be float greater on equal to 0 and lower than 1')

        request = self.factory.post('create_tax', {'tax_value': set()}, format='json')
        response = self.view(request)
        self.assertEqual(Tax.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'],
                         'Tax value error: tax_value should be float greater on equal to 0 and lower than 1')

    def test_create_tax_with_float_greater_than_1_or_lower_than_0_as_value(self):
        request = self.factory.post('create_tax', {'tax_value': 1.1}, format='json')
        response = self.view(request)
        self.assertEqual(Tax.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'],
                         'Tax value error: tax_value should be float greater on equal to 0 and lower than 1')

        request = self.factory.post('create_tax', {'tax_value': -0.2}, format='json')
        response = self.view(request)
        self.assertEqual(Tax.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'],
                         'Tax value error: tax_value should be float greater on equal to 0 and lower than 1')

    def test_create_tax_without_value(self):
        request = self.factory.post('create_tax', {}, format='json')
        response = self.view(request)
        self.assertEqual(Tax.objects.count(), 0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'missing argument: tax_value')