from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate
from ...views import AddCustomer, Customer, Address
from django.contrib.auth.models import User


class AddCustomerTestCase(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = AddCustomer.as_view()
        self.user = User(username='test', password='test')
        self.user.save()

    def test_add_customer(self):
        request = self.factory.post('add_customer', {'country': 'Country', 'city': 'City', 'postal_code': '00-000',
                                                     'street': 'Street', 'building_number': 1, 'apartment_number': 2,
                                                     'name': 'Customer name'}, format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(Customer.objects.count(), 1)
        self.assertEqual(Address.objects.count(), 1)
        customer = Customer.objects.get(pk=1)
        self.assertEqual(response.data['status'], 'OK')
        self.assertEqual(response.data['customer']['name'], customer.name)
        self.assertEqual(response.data['customer']['app_id'], customer.app_id)
        self.assertEqual(response.data['customer']['address']['country'], customer.address.country)
        self.assertEqual(response.data['customer']['address']['city'], customer.address.city)
        self.assertEqual(response.data['customer']['address']['postal_code'], customer.address.postal_code)
        self.assertEqual(response.data['customer']['address']['street'], customer.address.street)
        self.assertEqual(response.data['customer']['address']['building_number'], customer.address.building_number)
        self.assertEqual(response.data['customer']['address']['apartment_number'], customer.address.apartment_number)
        self.assertEqual(customer.name, 'Customer name')
        self.assertEqual(customer.address.country, 'Country')
        self.assertEqual(customer.address.city, 'City')
        self.assertEqual(customer.address.postal_code, '00-000')
        self.assertEqual(customer.address.street, 'Street')
        self.assertEqual(customer.address.building_number, 1)
        self.assertEqual(customer.address.apartment_number, 2)

    def test_add_customer_without_apartment_number(self):
        request = self.factory.post('add_customer', {'country': 'Country', 'city': 'City', 'postal_code': '00-000',
                                                     'street': 'Street', 'building_number': 1, 'name': 'Customer name'},
                                    format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(Customer.objects.count(), 1)
        self.assertEqual(Address.objects.count(), 1)
        customer = Customer.objects.get(pk=1)
        self.assertEqual(response.data['status'], 'OK')
        self.assertEqual(response.data['customer']['name'], customer.name)
        self.assertEqual(response.data['customer']['app_id'], customer.app_id)
        self.assertEqual(response.data['customer']['address']['country'], customer.address.country)
        self.assertEqual(response.data['customer']['address']['city'], customer.address.city)
        self.assertEqual(response.data['customer']['address']['postal_code'], customer.address.postal_code)
        self.assertEqual(response.data['customer']['address']['street'], customer.address.street)
        self.assertEqual(response.data['customer']['address']['building_number'], customer.address.building_number)
        self.assertEqual(response.data['customer']['address']['apartment_number'], customer.address.apartment_number)
        self.assertEqual(customer.name, 'Customer name')
        self.assertEqual(customer.address.country, 'Country')
        self.assertEqual(customer.address.city, 'City')
        self.assertEqual(customer.address.postal_code, '00-000')
        self.assertEqual(customer.address.street, 'Street')
        self.assertEqual(customer.address.building_number, 1)
        self.assertEqual(customer.address.apartment_number, None)

    def test_add_second_customer_with_same_name(self):
        request = self.factory.post('add_customer', {'country': 'Country', 'city': 'City', 'postal_code': '00-000',
                                                     'street': 'Street', 'building_number': 1, 'name': 'Customer name'},
                                    format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(Customer.objects.count(), 1)
        self.assertEqual(Address.objects.count(), 1)
        customer = Customer.objects.get(pk=1)
        self.assertEqual(response.data['status'], 'OK')
        self.assertEqual(response.data['customer']['name'], customer.name)
        self.assertEqual(response.data['customer']['app_id'], customer.app_id)
        self.assertEqual(response.data['customer']['address']['country'], customer.address.country)
        self.assertEqual(response.data['customer']['address']['city'], customer.address.city)
        self.assertEqual(response.data['customer']['address']['postal_code'], customer.address.postal_code)
        self.assertEqual(response.data['customer']['address']['street'], customer.address.street)
        self.assertEqual(response.data['customer']['address']['building_number'], customer.address.building_number)
        self.assertEqual(response.data['customer']['address']['apartment_number'], customer.address.apartment_number)
        self.assertEqual(customer.name, 'Customer name')
        self.assertEqual(customer.address.country, 'Country')
        self.assertEqual(customer.address.city, 'City')
        self.assertEqual(customer.address.postal_code, '00-000')
        self.assertEqual(customer.address.street, 'Street')
        self.assertEqual(customer.address.building_number, 1)
        self.assertEqual(customer.address.apartment_number, None)

        request = self.factory.post('add_customer', {'country': 'Country', 'city': 'City', 'postal_code': '00-000',
                                                     'street': 'Street', 'building_number': 2, 'name': 'Customer name'},
                                    format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(Customer.objects.count(), 2)
        self.assertEqual(Address.objects.count(), 2)
        customer = Customer.objects.get(pk=2)
        self.assertEqual(response.data['status'], 'OK')
        self.assertEqual(response.data['customer']['name'], customer.name)
        self.assertEqual(response.data['customer']['app_id'], customer.app_id)
        self.assertEqual(response.data['customer']['address']['country'], customer.address.country)
        self.assertEqual(response.data['customer']['address']['city'], customer.address.city)
        self.assertEqual(response.data['customer']['address']['postal_code'], customer.address.postal_code)
        self.assertEqual(response.data['customer']['address']['street'], customer.address.street)
        self.assertEqual(response.data['customer']['address']['building_number'], customer.address.building_number)
        self.assertEqual(response.data['customer']['address']['apartment_number'], customer.address.apartment_number)
        self.assertEqual(customer.name, 'Customer name')
        self.assertEqual(customer.address.country, 'Country')
        self.assertEqual(customer.address.city, 'City')
        self.assertEqual(customer.address.postal_code, '00-000')
        self.assertEqual(customer.address.street, 'Street')
        self.assertEqual(customer.address.building_number, 2)
        self.assertEqual(customer.address.apartment_number, None)

    def test_add_second_customer_with_same_address(self):
        request = self.factory.post('add_customer', {'country': 'Country', 'city': 'City', 'postal_code': '00-000',
                                                     'street': 'Street', 'building_number': 1, 'name': 'Customer name'},
                                    format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(Customer.objects.count(), 1)
        self.assertEqual(Address.objects.count(), 1)
        customer = Customer.objects.get(pk=1)
        self.assertEqual(response.data['status'], 'OK')
        self.assertEqual(response.data['customer']['name'], customer.name)
        self.assertEqual(response.data['customer']['app_id'], customer.app_id)
        self.assertEqual(response.data['customer']['address']['country'], customer.address.country)
        self.assertEqual(response.data['customer']['address']['city'], customer.address.city)
        self.assertEqual(response.data['customer']['address']['postal_code'], customer.address.postal_code)
        self.assertEqual(response.data['customer']['address']['street'], customer.address.street)
        self.assertEqual(response.data['customer']['address']['building_number'], customer.address.building_number)
        self.assertEqual(response.data['customer']['address']['apartment_number'], customer.address.apartment_number)
        self.assertEqual(customer.name, 'Customer name')
        self.assertEqual(customer.address.country, 'Country')
        self.assertEqual(customer.address.city, 'City')
        self.assertEqual(customer.address.postal_code, '00-000')
        self.assertEqual(customer.address.street, 'Street')
        self.assertEqual(customer.address.building_number, 1)
        self.assertEqual(customer.address.apartment_number, None)

        request = self.factory.post('add_customer', {'country': 'Country', 'city': 'City', 'postal_code': '00-000',
                                                     'street': 'Street', 'building_number': 1,
                                                     'name': 'Second customer name'}, format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(Customer.objects.count(), 2)
        self.assertEqual(Address.objects.count(), 2)
        customer = Customer.objects.get(pk=2)
        self.assertEqual(response.data['status'], 'OK')
        self.assertEqual(response.data['customer']['name'], customer.name)
        self.assertEqual(response.data['customer']['app_id'], customer.app_id)
        self.assertEqual(response.data['customer']['address']['country'], customer.address.country)
        self.assertEqual(response.data['customer']['address']['city'], customer.address.city)
        self.assertEqual(response.data['customer']['address']['postal_code'], customer.address.postal_code)
        self.assertEqual(response.data['customer']['address']['street'], customer.address.street)
        self.assertEqual(response.data['customer']['address']['building_number'], customer.address.building_number)
        self.assertEqual(response.data['customer']['address']['apartment_number'], customer.address.apartment_number)
        self.assertEqual(customer.name, 'Second customer name')
        self.assertEqual(customer.address.country, 'Country')
        self.assertEqual(customer.address.city, 'City')
        self.assertEqual(customer.address.postal_code, '00-000')
        self.assertEqual(customer.address.street, 'Street')
        self.assertEqual(customer.address.building_number, 1)
        self.assertEqual(customer.address.apartment_number, None)

    def test_add_second_customer_with_identical_data(self):
        request = self.factory.post('add_customer', {'country': 'Country', 'city': 'City', 'postal_code': '00-000',
                                                     'street': 'Street', 'building_number': 1, 'name': 'Customer name'},
                                    format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(Customer.objects.count(), 1)
        self.assertEqual(Address.objects.count(), 1)
        customer = Customer.objects.get(pk=1)
        self.assertEqual(response.data['status'], 'OK')
        self.assertEqual(response.data['customer']['name'], customer.name)
        self.assertEqual(response.data['customer']['app_id'], customer.app_id)
        self.assertEqual(response.data['customer']['address']['country'], customer.address.country)
        self.assertEqual(response.data['customer']['address']['city'], customer.address.city)
        self.assertEqual(response.data['customer']['address']['postal_code'], customer.address.postal_code)
        self.assertEqual(response.data['customer']['address']['street'], customer.address.street)
        self.assertEqual(response.data['customer']['address']['building_number'], customer.address.building_number)
        self.assertEqual(response.data['customer']['address']['apartment_number'], customer.address.apartment_number)
        self.assertEqual(customer.name, 'Customer name')
        self.assertEqual(customer.address.country, 'Country')
        self.assertEqual(customer.address.city, 'City')
        self.assertEqual(customer.address.postal_code, '00-000')
        self.assertEqual(customer.address.street, 'Street')
        self.assertEqual(customer.address.building_number, 1)
        self.assertEqual(customer.address.apartment_number, None)

        request = self.factory.post('add_customer', {'country': 'Country', 'city': 'City', 'postal_code': '00-000',
                                                     'street': 'Street', 'building_number': 1, 'name': 'Customer name'},
                                    format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(Customer.objects.count(), 1)
        self.assertEqual(Address.objects.count(), 1)
        second_customer = Customer.objects.get(pk=1)
        self.assertEqual(response.data['status'], 'OK')
        self.assertEqual(response.data['customer']['name'], second_customer.name)
        self.assertEqual(response.data['customer']['app_id'], second_customer.app_id)
        self.assertEqual(response.data['customer']['address']['country'], second_customer.address.country)
        self.assertEqual(response.data['customer']['address']['city'], second_customer.address.city)
        self.assertEqual(response.data['customer']['address']['postal_code'], second_customer.address.postal_code)
        self.assertEqual(response.data['customer']['address']['street'], second_customer.address.street)
        self.assertEqual(response.data['customer']['address']['building_number'],
                         second_customer.address.building_number)
        self.assertEqual(response.data['customer']['address']['apartment_number'],
                         second_customer.address.apartment_number)
        self.assertEqual(customer.name, second_customer.name)
        self.assertEqual(customer.address.country, second_customer.address.country)
        self.assertEqual(customer.address.city, second_customer.address.city)
        self.assertEqual(customer.address.postal_code, second_customer.address.postal_code)
        self.assertEqual(customer.address.street, second_customer.address.street)
        self.assertEqual(customer.address.building_number, second_customer.address.building_number)
        self.assertEqual(customer.address.apartment_number, second_customer.address.apartment_number)

    def test_add_customer_not_string_as_country(self):
        request = self.factory.post('add_customer', {'country': 1, 'city': 'City', 'postal_code': '00-000',
                                                     'street': 'Street', 'building_number': 1, 'name': 'Customer name'},
                                    format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Country error')
        self.assertEqual(Address.objects.count(), 0)
        self.assertEqual(Customer.objects.count(), 0)

        request = self.factory.post('add_customer', {'country': 0, 'city': 'City', 'postal_code': '00-000',
                                                     'street': 'Street', 'building_number': 1, 'name': 'Customer name'},
                                    format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Country error')
        self.assertEqual(Address.objects.count(), 0)
        self.assertEqual(Customer.objects.count(), 0)

        request = self.factory.post('add_customer', {'country': -1, 'city': 'City', 'postal_code': '00-000',
                                                     'street': 'Street', 'building_number': 1, 'name': 'Customer name'},
                                    format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Country error')
        self.assertEqual(Address.objects.count(), 0)
        self.assertEqual(Customer.objects.count(), 0)

        request = self.factory.post('add_customer', {'country': 1.1, 'city': 'City', 'postal_code': '00-000',
                                                     'street': 'Street', 'building_number': 1, 'name': 'Customer name'},
                                    format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Country error')
        self.assertEqual(Address.objects.count(), 0)
        self.assertEqual(Customer.objects.count(), 0)

        request = self.factory.post('add_customer', {'country': 1.1, 'city': 'City', 'postal_code': '00-000',
                                                     'street': 'Street', 'building_number': 1, 'name': 'Customer name'},
                                    format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Country error')
        self.assertEqual(Address.objects.count(), 0)
        self.assertEqual(Customer.objects.count(), 0)

        request = self.factory.post('add_customer', {'country': True, 'city': 'City', 'postal_code': '00-000',
                                                     'street': 'Street', 'building_number': 1, 'name': 'Customer name'},
                                    format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Country error')
        self.assertEqual(Address.objects.count(), 0)
        self.assertEqual(Customer.objects.count(), 0)

        request = self.factory.post('add_customer', {'country': False, 'city': 'City', 'postal_code': '00-000',
                                                     'street': 'Street', 'building_number': 1, 'name': 'Customer name'},
                                    format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Country error')
        self.assertEqual(Address.objects.count(), 0)
        self.assertEqual(Customer.objects.count(), 0)

        request = self.factory.post('add_customer', {'country': None, 'city': 'City', 'postal_code': '00-000',
                                                     'street': 'Street', 'building_number': 1, 'name': 'Customer name'},
                                    format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Country error')
        self.assertEqual(Address.objects.count(), 0)
        self.assertEqual(Customer.objects.count(), 0)

        request = self.factory.post('add_customer', {'country': list(), 'city': 'City', 'postal_code': '00-000',
                                                     'street': 'Street', 'building_number': 1, 'name': 'Customer name'},
                                    format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Country error')
        self.assertEqual(Address.objects.count(), 0)
        self.assertEqual(Customer.objects.count(), 0)

        request = self.factory.post('add_customer', {'country': tuple(), 'city': 'City', 'postal_code': '00-000',
                                                     'street': 'Street', 'building_number': 1, 'name': 'Customer name'},
                                    format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Country error')
        self.assertEqual(Address.objects.count(), 0)
        self.assertEqual(Customer.objects.count(), 0)

        request = self.factory.post('add_customer', {'country': dict(), 'city': 'City', 'postal_code': '00-000',
                                                     'street': 'Street', 'building_number': 1, 'name': 'Customer name'},
                                    format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Country error')
        self.assertEqual(Address.objects.count(), 0)
        self.assertEqual(Customer.objects.count(), 0)

        request = self.factory.post('add_customer', {'country': set(), 'city': 'City', 'postal_code': '00-000',
                                                     'street': 'Street', 'building_number': 1, 'name': 'Customer name'},
                                    format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Country error')
        self.assertEqual(Address.objects.count(), 0)
        self.assertEqual(Customer.objects.count(), 0)

    def test_add_customer_with_too_long_string_as_country(self):
        request = self.factory.post('add_customer', {'country': '1' * 51, 'city': 'City', 'postal_code': '00-000',
                                                     'street': 'Street', 'building_number': 1, 'name': 'Customer name'},
                                    format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Country error')
        self.assertEqual(Address.objects.count(), 0)
        self.assertEqual(Customer.objects.count(), 0)

    def test_add_customer_with_empty_string_as_country(self):
        request = self.factory.post('add_customer', {'country': '', 'city': 'City', 'postal_code': '00-000',
                                                     'street': 'Street', 'building_number': 1, 'name': 'Customer name'},
                                    format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Country error')
        self.assertEqual(Address.objects.count(), 0)
        self.assertEqual(Customer.objects.count(), 0)

        request = self.factory.post('add_customer', {'country': ' ', 'city': 'City', 'postal_code': '00-000',
                                                     'street': 'Street', 'building_number': 1, 'name': 'Customer name'},
                                    format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Country error')
        self.assertEqual(Address.objects.count(), 0)
        self.assertEqual(Customer.objects.count(), 0)

    def test_add_customer_with_not_string_as_city(self):
        request = self.factory.post('add_customer', {'country': 'Country', 'city': 1, 'postal_code': '00-000',
                                                     'street': 'Street', 'building_number': 1, 'name': 'Customer name'},
                                    format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'City error')
        self.assertEqual(Address.objects.count(), 0)
        self.assertEqual(Customer.objects.count(), 0)

        request = self.factory.post('add_customer', {'country': 'Country', 'city': 0, 'postal_code': '00-000',
                                                     'street': 'Street', 'building_number': 1, 'name': 'Customer name'},
                                    format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'City error')
        self.assertEqual(Address.objects.count(), 0)
        self.assertEqual(Customer.objects.count(), 0)

        request = self.factory.post('add_customer', {'country': 'Country', 'city': -1, 'postal_code': '00-000',
                                                     'street': 'Street', 'building_number': 1, 'name': 'Customer name'},
                                    format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'City error')
        self.assertEqual(Address.objects.count(), 0)
        self.assertEqual(Customer.objects.count(), 0)

        request = self.factory.post('add_customer', {'country': 'Country', 'city': 1.1, 'postal_code': '00-000',
                                                     'street': 'Street', 'building_number': 1, 'name': 'Customer name'},
                                    format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'City error')
        self.assertEqual(Address.objects.count(), 0)
        self.assertEqual(Customer.objects.count(), 0)

        request = self.factory.post('add_customer', {'country': 'Country', 'city': -1.1, 'postal_code': '00-000',
                                                     'street': 'Street', 'building_number': 1, 'name': 'Customer name'},
                                    format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'City error')
        self.assertEqual(Address.objects.count(), 0)
        self.assertEqual(Customer.objects.count(), 0)

        request = self.factory.post('add_customer', {'country': 'Country', 'city': True, 'postal_code': '00-000',
                                                     'street': 'Street', 'building_number': 1, 'name': 'Customer name'},
                                    format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'City error')
        self.assertEqual(Address.objects.count(), 0)
        self.assertEqual(Customer.objects.count(), 0)

        request = self.factory.post('add_customer', {'country': 'Country', 'city': False, 'postal_code': '00-000',
                                                     'street': 'Street', 'building_number': 1, 'name': 'Customer name'},
                                    format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'City error')
        self.assertEqual(Address.objects.count(), 0)
        self.assertEqual(Customer.objects.count(), 0)

        request = self.factory.post('add_customer', {'country': 'Country', 'city': None, 'postal_code': '00-000',
                                                     'street': 'Street', 'building_number': 1, 'name': 'Customer name'},
                                    format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'City error')
        self.assertEqual(Address.objects.count(), 0)
        self.assertEqual(Customer.objects.count(), 0)

        request = self.factory.post('add_customer', {'country': 'Country', 'city': list(), 'postal_code': '00-000',
                                                     'street': 'Street', 'building_number': 1, 'name': 'Customer name'},
                                    format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'City error')
        self.assertEqual(Address.objects.count(), 0)
        self.assertEqual(Customer.objects.count(), 0)

        request = self.factory.post('add_customer', {'country': 'Country', 'city': tuple(), 'postal_code': '00-000',
                                                     'street': 'Street', 'building_number': 1, 'name': 'Customer name'},
                                    format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'City error')
        self.assertEqual(Address.objects.count(), 0)
        self.assertEqual(Customer.objects.count(), 0)

        request = self.factory.post('add_customer', {'country': 'Country', 'city': dict(), 'postal_code': '00-000',
                                                     'street': 'Street', 'building_number': 1, 'name': 'Customer name'},
                                    format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'City error')
        self.assertEqual(Address.objects.count(), 0)
        self.assertEqual(Customer.objects.count(), 0)

        request = self.factory.post('add_customer', {'country': 'Country', 'city': set(), 'postal_code': '00-000',
                                                     'street': 'Street', 'building_number': 1, 'name': 'Customer name'},
                                    format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'City error')
        self.assertEqual(Address.objects.count(), 0)
        self.assertEqual(Customer.objects.count(), 0)

    def test_add_customer_with_too_long_string_as_city(self):
        request = self.factory.post('add_customer', {'country': 'Country', 'city': '1' * 101, 'postal_code': '00-000',
                                                     'street': 'Street', 'building_number': 1, 'name': 'Customer name'},
                                    format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'City error')
        self.assertEqual(Address.objects.count(), 0)
        self.assertEqual(Customer.objects.count(), 0)

    def test_add_customer_with_empty_string_as_city(self):
        request = self.factory.post('add_customer', {'country': 'Country', 'city': '', 'postal_code': '00-000',
                                                     'street': 'Street', 'building_number': 1, 'name': 'Customer name'},
                                    format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'City error')
        self.assertEqual(Address.objects.count(), 0)
        self.assertEqual(Customer.objects.count(), 0)

        request = self.factory.post('add_customer', {'country': 'Country', 'city': ' ', 'postal_code': '00-000',
                                                     'street': 'Street', 'building_number': 1, 'name': 'Customer name'},
                                    format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'City error')
        self.assertEqual(Address.objects.count(), 0)
        self.assertEqual(Customer.objects.count(), 0)

    def test_add_customer_with_not_string_as_postal_code(self):
        request = self.factory.post('add_customer', {'country': 'Country', 'city': 'City', 'postal_code': 1,
                                                     'street': 'Street', 'building_number': 1, 'name': 'Customer name'},
                                    format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Postal code error')
        self.assertEqual(Address.objects.count(), 0)
        self.assertEqual(Customer.objects.count(), 0)

        request = self.factory.post('add_customer', {'country': 'Country', 'city': 'City', 'postal_code': 0,
                                                     'street': 'Street', 'building_number': 1, 'name': 'Customer name'},
                                    format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Postal code error')
        self.assertEqual(Address.objects.count(), 0)
        self.assertEqual(Customer.objects.count(), 0)

        request = self.factory.post('add_customer', {'country': 'Country', 'city': 'City', 'postal_code': -1,
                                                     'street': 'Street', 'building_number': 1, 'name': 'Customer name'},
                                    format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Postal code error')
        self.assertEqual(Address.objects.count(), 0)
        self.assertEqual(Customer.objects.count(), 0)

        request = self.factory.post('add_customer', {'country': 'Country', 'city': 'City', 'postal_code': 1.1,
                                                     'street': 'Street', 'building_number': 1, 'name': 'Customer name'},
                                    format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Postal code error')
        self.assertEqual(Address.objects.count(), 0)
        self.assertEqual(Customer.objects.count(), 0)

        request = self.factory.post('add_customer', {'country': 'Country', 'city': 'City', 'postal_code': -1.1,
                                                     'street': 'Street', 'building_number': 1, 'name': 'Customer name'},
                                    format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Postal code error')
        self.assertEqual(Address.objects.count(), 0)
        self.assertEqual(Customer.objects.count(), 0)

        request = self.factory.post('add_customer', {'country': 'Country', 'city': 'City', 'postal_code': True,
                                                     'street': 'Street', 'building_number': 1, 'name': 'Customer name'},
                                    format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Postal code error')
        self.assertEqual(Address.objects.count(), 0)
        self.assertEqual(Customer.objects.count(), 0)

        request = self.factory.post('add_customer', {'country': 'Country', 'city': 'City', 'postal_code': False,
                                                     'street': 'Street', 'building_number': 1, 'name': 'Customer name'},
                                    format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Postal code error')
        self.assertEqual(Address.objects.count(), 0)
        self.assertEqual(Customer.objects.count(), 0)

        request = self.factory.post('add_customer', {'country': 'Country', 'city': 'City', 'postal_code': None,
                                                     'street': 'Street', 'building_number': 1, 'name': 'Customer name'},
                                    format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Postal code error')
        self.assertEqual(Address.objects.count(), 0)
        self.assertEqual(Customer.objects.count(), 0)

        request = self.factory.post('add_customer', {'country': 'Country', 'city': 'City', 'postal_code': list(),
                                                     'street': 'Street', 'building_number': 1, 'name': 'Customer name'},
                                    format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Postal code error')
        self.assertEqual(Address.objects.count(), 0)
        self.assertEqual(Customer.objects.count(), 0)

        request = self.factory.post('add_customer', {'country': 'Country', 'city': 'City', 'postal_code': tuple(),
                                                     'street': 'Street', 'building_number': 1, 'name': 'Customer name'},
                                    format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Postal code error')
        self.assertEqual(Address.objects.count(), 0)
        self.assertEqual(Customer.objects.count(), 0)

        request = self.factory.post('add_customer', {'country': 'Country', 'city': 'City', 'postal_code': dict(),
                                                     'street': 'Street', 'building_number': 1, 'name': 'Customer name'},
                                    format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Postal code error')
        self.assertEqual(Address.objects.count(), 0)
        self.assertEqual(Customer.objects.count(), 0)

        request = self.factory.post('add_customer', {'country': 'Country', 'city': 'City', 'postal_code': set(),
                                                     'street': 'Street', 'building_number': 1, 'name': 'Customer name'},
                                    format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Postal code error')
        self.assertEqual(Address.objects.count(), 0)
        self.assertEqual(Customer.objects.count(), 0)

    def test_add_customer_with_too_long_string_as_postal_code(self):
        request = self.factory.post('add_customer', {'country': 'Country', 'city': 'City', 'postal_code': '1' * 7,
                                                     'street': 'Street', 'building_number': 1, 'name': 'Customer name'},
                                    format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Postal code error')
        self.assertEqual(Address.objects.count(), 0)
        self.assertEqual(Customer.objects.count(), 0)

    def test_add_customer_with_empty_string_as_postal_code(self):
        request = self.factory.post('add_customer', {'country': 'Country', 'city': 'City', 'postal_code': '',
                                                     'street': 'Street', 'building_number': 1, 'name': 'Customer name'},
                                    format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Postal code error')
        self.assertEqual(Address.objects.count(), 0)
        self.assertEqual(Customer.objects.count(), 0)

        request = self.factory.post('add_customer', {'country': 'Country', 'city': 'City', 'postal_code': ' ',
                                                     'street': 'Street', 'building_number': 1, 'name': 'Customer name'},
                                    format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Postal code error')
        self.assertEqual(Address.objects.count(), 0)
        self.assertEqual(Customer.objects.count(), 0)

    def test_add_customer_with_not_string_as_street(self):
        request = self.factory.post('add_customer', {'country': 'Country', 'city': 'City', 'postal_code': '00-000',
                                                     'street': 1, 'building_number': 1, 'name': 'Customer name'},
                                    format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Street error')
        self.assertEqual(Address.objects.count(), 0)
        self.assertEqual(Customer.objects.count(), 0)

        request = self.factory.post('add_customer', {'country': 'Country', 'city': 'City', 'postal_code': '00-000',
                                                     'street': 0, 'building_number': 1, 'name': 'Customer name'},
                                    format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Street error')
        self.assertEqual(Address.objects.count(), 0)
        self.assertEqual(Customer.objects.count(), 0)

        request = self.factory.post('add_customer', {'country': 'Country', 'city': 'City', 'postal_code': '00-000',
                                                     'street': -1, 'building_number': 1, 'name': 'Customer name'},
                                    format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Street error')
        self.assertEqual(Address.objects.count(), 0)
        self.assertEqual(Customer.objects.count(), 0)

        request = self.factory.post('add_customer', {'country': 'Country', 'city': 'City', 'postal_code': '00-000',
                                                     'street': 1.1, 'building_number': 1, 'name': 'Customer name'},
                                    format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Street error')
        self.assertEqual(Address.objects.count(), 0)
        self.assertEqual(Customer.objects.count(), 0)

        request = self.factory.post('add_customer', {'country': 'Country', 'city': 'City', 'postal_code': '00-000',
                                                     'street': -1.1, 'building_number': 1, 'name': 'Customer name'},
                                    format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Street error')
        self.assertEqual(Address.objects.count(), 0)
        self.assertEqual(Customer.objects.count(), 0)

        request = self.factory.post('add_customer', {'country': 'Country', 'city': 'City', 'postal_code': '00-000',
                                                     'street': True, 'building_number': 1, 'name': 'Customer name'},
                                    format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Street error')
        self.assertEqual(Address.objects.count(), 0)
        self.assertEqual(Customer.objects.count(), 0)

        request = self.factory.post('add_customer', {'country': 'Country', 'city': 'City', 'postal_code': '00-000',
                                                     'street': False, 'building_number': 1, 'name': 'Customer name'},
                                    format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Street error')
        self.assertEqual(Address.objects.count(), 0)
        self.assertEqual(Customer.objects.count(), 0)

        request = self.factory.post('add_customer', {'country': 'Country', 'city': 'City', 'postal_code': '00-000',
                                                     'street': None, 'building_number': 1, 'name': 'Customer name'},
                                    format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Street error')
        self.assertEqual(Address.objects.count(), 0)
        self.assertEqual(Customer.objects.count(), 0)

        request = self.factory.post('add_customer', {'country': 'Country', 'city': 'City', 'postal_code': '00-000',
                                                     'street': list(), 'building_number': 1, 'name': 'Customer name'},
                                    format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Street error')
        self.assertEqual(Address.objects.count(), 0)
        self.assertEqual(Customer.objects.count(), 0)

        request = self.factory.post('add_customer', {'country': 'Country', 'city': 'City', 'postal_code': '00-000',
                                                     'street': tuple(), 'building_number': 1, 'name': 'Customer name'},
                                    format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Street error')
        self.assertEqual(Address.objects.count(), 0)
        self.assertEqual(Customer.objects.count(), 0)

        request = self.factory.post('add_customer', {'country': 'Country', 'city': 'City', 'postal_code': '00-000',
                                                     'street': dict(), 'building_number': 1, 'name': 'Customer name'},
                                    format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Street error')
        self.assertEqual(Address.objects.count(), 0)
        self.assertEqual(Customer.objects.count(), 0)

        request = self.factory.post('add_customer', {'country': 'Country', 'city': 'City', 'postal_code': '00-000',
                                                     'street': set(), 'building_number': 1, 'name': 'Customer name'},
                                    format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Street error')
        self.assertEqual(Address.objects.count(), 0)
        self.assertEqual(Customer.objects.count(), 0)

    def test_add_customer_with_too_long_string_as_street(self):
        request = self.factory.post('add_customer', {'country': 'Country', 'city': 'City', 'postal_code': '00-000',
                                                     'street': '1' * 101, 'building_number': 1, 'name':
                                                         'Customer name'}, format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Street error')
        self.assertEqual(Address.objects.count(), 0)
        self.assertEqual(Customer.objects.count(), 0)

    def test_add_customer_with_empty_string_as_street(self):
        request = self.factory.post('add_customer', {'country': 'Country', 'city': 'City', 'postal_code': '00-000',
                                                     'street': '', 'building_number': 1, 'name': 'Customer name'},
                                    format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Street error')
        self.assertEqual(Address.objects.count(), 0)
        self.assertEqual(Customer.objects.count(), 0)

        request = self.factory.post('add_customer', {'country': 'Country', 'city': 'City', 'postal_code': '00-000',
                                                     'street': ' ', 'building_number': 1, 'name': 'Customer name'},
                                    format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Street error')
        self.assertEqual(Address.objects.count(), 0)
        self.assertEqual(Customer.objects.count(), 0)

    def test_add_customer_with_not_int_as_building_number(self):
        request = self.factory.post('add_customer', {'country': 'Country', 'city': 'City', 'postal_code': '00-000',
                                                     'street': 'Street', 'building_number': '',
                                                     'name': 'Customer name'}, format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Building number error')
        self.assertEqual(Address.objects.count(), 0)
        self.assertEqual(Customer.objects.count(), 0)

        request = self.factory.post('add_customer', {'country': 'Country', 'city': 'City', 'postal_code': '00-000',
                                                     'street': 'Street', 'building_number': ' ',
                                                     'name': 'Customer name'}, format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Building number error')
        self.assertEqual(Address.objects.count(), 0)
        self.assertEqual(Customer.objects.count(), 0)

        request = self.factory.post('add_customer', {'country': 'Country', 'city': 'City', 'postal_code': '00-000',
                                                     'street': 'Street', 'building_number': '1',
                                                     'name': 'Customer name'}, format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Building number error')
        self.assertEqual(Address.objects.count(), 0)
        self.assertEqual(Customer.objects.count(), 0)

        request = self.factory.post('add_customer', {'country': 'Country', 'city': 'City', 'postal_code': '00-000',
                                                     'street': 'Street', 'building_number': '0',
                                                     'name': 'Customer name'}, format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Building number error')
        self.assertEqual(Address.objects.count(), 0)
        self.assertEqual(Customer.objects.count(), 0)

        request = self.factory.post('add_customer', {'country': 'Country', 'city': 'City', 'postal_code': '00-000',
                                                     'street': 'Street', 'building_number': '-1',
                                                     'name': 'Customer name'}, format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Building number error')
        self.assertEqual(Address.objects.count(), 0)
        self.assertEqual(Customer.objects.count(), 0)

        request = self.factory.post('add_customer', {'country': 'Country', 'city': 'City', 'postal_code': '00-000',
                                                     'street': 'Street', 'building_number': '1.1',
                                                     'name': 'Customer name'}, format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Building number error')
        self.assertEqual(Address.objects.count(), 0)
        self.assertEqual(Customer.objects.count(), 0)

        request = self.factory.post('add_customer', {'country': 'Country', 'city': 'City', 'postal_code': '00-000',
                                                     'street': 'Street', 'building_number': '-1.1',
                                                     'name': 'Customer name'}, format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Building number error')
        self.assertEqual(Address.objects.count(), 0)
        self.assertEqual(Customer.objects.count(), 0)

        request = self.factory.post('add_customer', {'country': 'Country', 'city': 'City', 'postal_code': '00-000',
                                                     'street': 'Street', 'building_number': 'Text',
                                                     'name': 'Customer name'}, format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Building number error')
        self.assertEqual(Address.objects.count(), 0)
        self.assertEqual(Customer.objects.count(), 0)

        request = self.factory.post('add_customer', {'country': 'Country', 'city': 'City', 'postal_code': '00-000',
                                                     'street': 'Street', 'building_number': 1.1,
                                                     'name': 'Customer name'}, format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Building number error')
        self.assertEqual(Address.objects.count(), 0)
        self.assertEqual(Customer.objects.count(), 0)

        request = self.factory.post('add_customer', {'country': 'Country', 'city': 'City', 'postal_code': '00-000',
                                                     'street': 'Street', 'building_number': -1.1,
                                                     'name': 'Customer name'}, format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Building number error')
        self.assertEqual(Address.objects.count(), 0)
        self.assertEqual(Customer.objects.count(), 0)

        request = self.factory.post('add_customer', {'country': 'Country', 'city': 'City', 'postal_code': '00-000',
                                                     'street': 'Street', 'building_number': True,
                                                     'name': 'Customer name'}, format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Building number error')
        self.assertEqual(Address.objects.count(), 0)
        self.assertEqual(Customer.objects.count(), 0)

        request = self.factory.post('add_customer', {'country': 'Country', 'city': 'City', 'postal_code': '00-000',
                                                     'street': 'Street', 'building_number': False,
                                                     'name': 'Customer name'}, format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Building number error')
        self.assertEqual(Address.objects.count(), 0)
        self.assertEqual(Customer.objects.count(), 0)

        request = self.factory.post('add_customer', {'country': 'Country', 'city': 'City', 'postal_code': '00-000',
                                                     'street': 'Street', 'building_number': None,
                                                     'name': 'Customer name'}, format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Building number error')
        self.assertEqual(Address.objects.count(), 0)
        self.assertEqual(Customer.objects.count(), 0)

        request = self.factory.post('add_customer', {'country': 'Country', 'city': 'City', 'postal_code': '00-000',
                                                     'street': 'Street', 'building_number': list(),
                                                     'name': 'Customer name'}, format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Building number error')
        self.assertEqual(Address.objects.count(), 0)
        self.assertEqual(Customer.objects.count(), 0)

        request = self.factory.post('add_customer', {'country': 'Country', 'city': 'City', 'postal_code': '00-000',
                                                     'street': 'Street', 'building_number': tuple(),
                                                     'name': 'Customer name'}, format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Building number error')
        self.assertEqual(Address.objects.count(), 0)
        self.assertEqual(Customer.objects.count(), 0)

        request = self.factory.post('add_customer', {'country': 'Country', 'city': 'City', 'postal_code': '00-000',
                                                     'street': 'Street', 'building_number': dict(),
                                                     'name': 'Customer name'}, format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Building number error')
        self.assertEqual(Address.objects.count(), 0)
        self.assertEqual(Customer.objects.count(), 0)

        request = self.factory.post('add_customer', {'country': 'Country', 'city': 'City', 'postal_code': '00-000',
                                                     'street': 'Street', 'building_number': set(),
                                                     'name': 'Customer name'}, format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Building number error')
        self.assertEqual(Address.objects.count(), 0)
        self.assertEqual(Customer.objects.count(), 0)

    def test_add_customer_with_negative_int_or_0_as_building_number(self):
        request = self.factory.post('add_customer', {'country': 'Country', 'city': 'City', 'postal_code': '00-000',
                                                     'street': 'Street', 'building_number': -1,
                                                     'name': 'Customer name'}, format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Building number error')
        self.assertEqual(Address.objects.count(), 0)
        self.assertEqual(Customer.objects.count(), 0)

        request = self.factory.post('add_customer', {'country': 'Country', 'city': 'City', 'postal_code': '00-000',
                                                     'street': 'Street', 'building_number': 0,
                                                     'name': 'Customer name'}, format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Building number error')
        self.assertEqual(Address.objects.count(), 0)
        self.assertEqual(Customer.objects.count(), 0)

    def test_add_customer_with_not_int_or_None_as_apartment_number(self):
        request = self.factory.post('add_customer', {'country': 'Country', 'city': 'City', 'postal_code': '00-000',
                                                     'street': 'Street', 'building_number': 1, 'apartment_number': '',
                                                     'name': 'Customer name'}, format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Apartment number error')
        self.assertEqual(Address.objects.count(), 0)
        self.assertEqual(Customer.objects.count(), 0)

        request = self.factory.post('add_customer', {'country': 'Country', 'city': 'City', 'postal_code': '00-000',
                                                     'street': 'Street', 'building_number': 1, 'apartment_number': ' ',
                                                     'name': 'Customer name'}, format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Apartment number error')
        self.assertEqual(Address.objects.count(), 0)
        self.assertEqual(Customer.objects.count(), 0)

        request = self.factory.post('add_customer', {'country': 'Country', 'city': 'City', 'postal_code': '00-000',
                                                     'street': 'Street', 'building_number': 1, 'apartment_number': '1',
                                                     'name': 'Customer name'}, format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Apartment number error')
        self.assertEqual(Address.objects.count(), 0)
        self.assertEqual(Customer.objects.count(), 0)

        request = self.factory.post('add_customer', {'country': 'Country', 'city': 'City', 'postal_code': '00-000',
                                                     'street': 'Street', 'building_number': 1, 'apartment_number': '0',
                                                     'name': 'Customer name'}, format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Apartment number error')
        self.assertEqual(Address.objects.count(), 0)
        self.assertEqual(Customer.objects.count(), 0)

        request = self.factory.post('add_customer', {'country': 'Country', 'city': 'City', 'postal_code': '00-000',
                                                     'street': 'Street', 'building_number': 1, 'apartment_number': '-1',
                                                     'name': 'Customer name'}, format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Apartment number error')
        self.assertEqual(Address.objects.count(), 0)
        self.assertEqual(Customer.objects.count(), 0)

        request = self.factory.post('add_customer', {'country': 'Country', 'city': 'City', 'postal_code': '00-000',
                                                     'street': 'Street', 'building_number': 1,
                                                     'apartment_number': '1.1', 'name': 'Customer name'}, format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Apartment number error')
        self.assertEqual(Address.objects.count(), 0)
        self.assertEqual(Customer.objects.count(), 0)

        request = self.factory.post('add_customer', {'country': 'Country', 'city': 'City', 'postal_code': '00-000',
                                                     'street': 'Street', 'building_number': 1,
                                                     'apartment_number': '-1.1', 'name': 'Customer name'},
                                    format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Apartment number error')
        self.assertEqual(Address.objects.count(), 0)
        self.assertEqual(Customer.objects.count(), 0)

        request = self.factory.post('add_customer', {'country': 'Country', 'city': 'City', 'postal_code': '00-000',
                                                     'street': 'Street', 'building_number': 1,
                                                     'apartment_number': 'Text', 'name': 'Customer name'},
                                    format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Apartment number error')
        self.assertEqual(Address.objects.count(), 0)
        self.assertEqual(Customer.objects.count(), 0)

        request = self.factory.post('add_customer', {'country': 'Country', 'city': 'City', 'postal_code': '00-000',
                                                     'street': 'Street', 'building_number': 1, 'apartment_number': 1.1,
                                                     'name': 'Customer name'}, format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Apartment number error')
        self.assertEqual(Address.objects.count(), 0)
        self.assertEqual(Customer.objects.count(), 0)

        request = self.factory.post('add_customer', {'country': 'Country', 'city': 'City', 'postal_code': '00-000',
                                                     'street': 'Street', 'building_number': 1, 'apartment_number': -1.1,
                                                     'name': 'Customer name'}, format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Apartment number error')
        self.assertEqual(Address.objects.count(), 0)
        self.assertEqual(Customer.objects.count(), 0)

        request = self.factory.post('add_customer', {'country': 'Country', 'city': 'City', 'postal_code': '00-000',
                                                     'street': 'Street', 'building_number': 1, 'apartment_number': True,
                                                     'name': 'Customer name'}, format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Apartment number error')
        self.assertEqual(Address.objects.count(), 0)
        self.assertEqual(Customer.objects.count(), 0)

        request = self.factory.post('add_customer', {'country': 'Country', 'city': 'City', 'postal_code': '00-000',
                                                     'street': 'Street', 'building_number': 1,
                                                     'apartment_number': False, 'name': 'Customer name'}, format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Apartment number error')
        self.assertEqual(Address.objects.count(), 0)
        self.assertEqual(Customer.objects.count(), 0)

        request = self.factory.post('add_customer', {'country': 'Country', 'city': 'City', 'postal_code': '00-000',
                                                     'street': 'Street', 'building_number': 1,
                                                     'apartment_number': list(), 'name': 'Customer name'},
                                    format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Apartment number error')
        self.assertEqual(Address.objects.count(), 0)
        self.assertEqual(Customer.objects.count(), 0)

        request = self.factory.post('add_customer', {'country': 'Country', 'city': 'City', 'postal_code': '00-000',
                                                     'street': 'Street', 'building_number': 1,
                                                     'apartment_number': tuple(), 'name': 'Customer name'},
                                    format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Apartment number error')
        self.assertEqual(Address.objects.count(), 0)
        self.assertEqual(Customer.objects.count(), 0)

        request = self.factory.post('add_customer', {'country': 'Country', 'city': 'City', 'postal_code': '00-000',
                                                     'street': 'Street', 'building_number': 1,
                                                     'apartment_number': dict(), 'name': 'Customer name'},
                                    format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Apartment number error')
        self.assertEqual(Address.objects.count(), 0)
        self.assertEqual(Customer.objects.count(), 0)

        request = self.factory.post('add_customer', {'country': 'Country', 'city': 'City', 'postal_code': '00-000',
                                                     'street': 'Street', 'building_number': 1,
                                                     'apartment_number': set(), 'name': 'Customer name'}, format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Apartment number error')
        self.assertEqual(Address.objects.count(), 0)
        self.assertEqual(Customer.objects.count(), 0)

    def test_add_customer_with_negative_int_or_0_as_apartment_number(self):
        request = self.factory.post('add_customer', {'country': 'Country', 'city': 'City', 'postal_code': '00-000',
                                                     'street': 'Street', 'building_number': 1, 'apartment_number': -1,
                                                     'name': 'Customer name'}, format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Apartment number error')
        self.assertEqual(Address.objects.count(), 0)
        self.assertEqual(Customer.objects.count(), 0)

        request = self.factory.post('add_customer', {'country': 'Country', 'city': 'City', 'postal_code': '00-000',
                                                     'street': 'Street', 'building_number': 1, 'apartment_number': 0,
                                                     'name': 'Customer name'}, format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Apartment number error')
        self.assertEqual(Address.objects.count(), 0)
        self.assertEqual(Customer.objects.count(), 0)

    def test_add_customer_with_not_string_as_name(self):
        request = self.factory.post('add_customer', {'country': 'Country', 'city': 'City', 'postal_code': '00-000',
                                                     'street': 'Street', 'building_number': 1, 'name': 1},
                                    format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Name error')
        self.assertEqual(Address.objects.count(), 0)
        self.assertEqual(Customer.objects.count(), 0)

        request = self.factory.post('add_customer', {'country': 'Country', 'city': 'City', 'postal_code': '00-000',
                                                     'street': 'Street', 'building_number': 1, 'name': 0},
                                    format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Name error')
        self.assertEqual(Address.objects.count(), 0)
        self.assertEqual(Customer.objects.count(), 0)

        request = self.factory.post('add_customer', {'country': 'Country', 'city': 'City', 'postal_code': '00-000',
                                                     'street': 'Street', 'building_number': 1, 'name': -1},
                                    format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Name error')
        self.assertEqual(Address.objects.count(), 0)
        self.assertEqual(Customer.objects.count(), 0)

        request = self.factory.post('add_customer', {'country': 'Country', 'city': 'City', 'postal_code': '00-000',
                                                     'street': 'Street', 'building_number': 1, 'name': 1.1},
                                    format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Name error')
        self.assertEqual(Address.objects.count(), 0)
        self.assertEqual(Customer.objects.count(), 0)

        request = self.factory.post('add_customer', {'country': 'Country', 'city': 'City', 'postal_code': '00-000',
                                                     'street': 'Street', 'building_number': 1, 'name': -1.1},
                                    format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Name error')
        self.assertEqual(Address.objects.count(), 0)
        self.assertEqual(Customer.objects.count(), 0)

        request = self.factory.post('add_customer', {'country': 'Country', 'city': 'City', 'postal_code': '00-000',
                                                     'street': 'Street', 'building_number': 1, 'name': True},
                                    format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Name error')
        self.assertEqual(Address.objects.count(), 0)
        self.assertEqual(Customer.objects.count(), 0)

        request = self.factory.post('add_customer', {'country': 'Country', 'city': 'City', 'postal_code': '00-000',
                                                     'street': 'Street', 'building_number': 1, 'name': False},
                                    format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Name error')
        self.assertEqual(Address.objects.count(), 0)
        self.assertEqual(Customer.objects.count(), 0)

        request = self.factory.post('add_customer', {'country': 'Country', 'city': 'City', 'postal_code': '00-000',
                                                     'street': 'Street', 'building_number': 1, 'name': None},
                                    format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Name error')
        self.assertEqual(Address.objects.count(), 0)
        self.assertEqual(Customer.objects.count(), 0)

        request = self.factory.post('add_customer', {'country': 'Country', 'city': 'City', 'postal_code': '00-000',
                                                     'street': 'Street', 'building_number': 1, 'name': list()},
                                    format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Name error')
        self.assertEqual(Address.objects.count(), 0)
        self.assertEqual(Customer.objects.count(), 0)

        request = self.factory.post('add_customer', {'country': 'Country', 'city': 'City', 'postal_code': '00-000',
                                                     'street': 'Street', 'building_number': 1, 'name': tuple()},
                                    format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Name error')
        self.assertEqual(Address.objects.count(), 0)
        self.assertEqual(Customer.objects.count(), 0)

        request = self.factory.post('add_customer', {'country': 'Country', 'city': 'City', 'postal_code': '00-000',
                                                     'street': 'Street', 'building_number': 1, 'name': dict()},
                                    format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Name error')
        self.assertEqual(Address.objects.count(), 0)
        self.assertEqual(Customer.objects.count(), 0)

        request = self.factory.post('add_customer', {'country': 'Country', 'city': 'City', 'postal_code': '00-000',
                                                     'street': 'Street', 'building_number': 1, 'name': set()},
                                    format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Name error')
        self.assertEqual(Address.objects.count(), 0)
        self.assertEqual(Customer.objects.count(), 0)

    def test_add_customer_with_empty_string_as_name(self):
        request = self.factory.post('add_customer', {'country': 'Country', 'city': 'City', 'postal_code': '00-000',
                                                     'street': 'Street', 'building_number': 1, 'name': ''},
                                    format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Name error')
        self.assertEqual(Address.objects.count(), 0)
        self.assertEqual(Customer.objects.count(), 0)

        request = self.factory.post('add_customer', {'country': 'Country', 'city': 'City', 'postal_code': '00-000',
                                                     'street': 'Street', 'building_number': 1, 'name': ' '},
                                    format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'Name error')
        self.assertEqual(Address.objects.count(), 0)
        self.assertEqual(Customer.objects.count(), 0)

    def test_add_customer_with_missing_address_arguments(self):
        request = self.factory.post('add_customer', {'city': 'City', 'postal_code': '00-000', 'street': 'Street',
                                                     'building_number': 1, 'name': 'Customer name'}, format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'missing 1 required positional argument: \'country\'')
        self.assertEqual(Address.objects.count(), 0)
        self.assertEqual(Customer.objects.count(), 0)

        request = self.factory.post('add_customer', {'country': 'Country', 'postal_code': '00-000', 'street': 'Street',
                                                     'building_number': 1, 'name': 'Customer name'}, format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'missing 1 required positional argument: \'city\'')
        self.assertEqual(Address.objects.count(), 0)
        self.assertEqual(Customer.objects.count(), 0)

        request = self.factory.post('add_customer', {'country': 'Country', 'city': 'City', 'street': 'Street',
                                                     'building_number': 1, 'name': 'Customer'}, format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'missing 1 required positional argument: \'postal_code\'')
        self.assertEqual(Address.objects.count(), 0)
        self.assertEqual(Customer.objects.count(), 0)

        request = self.factory.post('add_customer', {'country': 'Country', 'city': 'City', 'postal_code': '00-000',
                                                     'building_number': 1, 'name': 'Customer'}, format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'missing 1 required positional argument: \'street\'')
        self.assertEqual(Address.objects.count(), 0)
        self.assertEqual(Customer.objects.count(), 0)

        request = self.factory.post('add_customer', {'country': 'Country', 'city': 'City', 'postal_code': '00-000',
                                                     'street': 'Street', 'name': 'Customer'}, format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'missing 1 required positional argument: \'building_number\'')
        self.assertEqual(Address.objects.count(), 0)
        self.assertEqual(Customer.objects.count(), 0)

    def test_add_customer_without_name_argument(self):
        request = self.factory.post('add_customer', {'country': 'Country', 'city': 'City', 'postal_code': '00-000',
                                                     'street': 'Street', 'building_number': 1}, format='json')
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'missing 1 required positional argument: \'name\'')
        self.assertEqual(Address.objects.count(), 0)
        self.assertEqual(Customer.objects.count(), 0)
