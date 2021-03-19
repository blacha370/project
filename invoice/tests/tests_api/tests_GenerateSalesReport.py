from rest_framework.test import APITestCase, APIRequestFactory
from ...views import (GenerateSalesReport, Invoice, Receipt, Transaction, Company, Customer, Marketplace,
                      SoldItem, Item, Tax, Address, datetime)


class GenerateSalesReportTestCase(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = GenerateSalesReport.as_view()
        address = Address.create(country='Country', city='City', postal_code='11-222', street='Street',
                                 building_number=1)
        self.company = Company.create(name='Company', address=address)
        address = Address.create(country='Country', city='City', postal_code='11-222', street='Street',
                                 building_number=2)
        self.customer = Customer.create(name='Customer', address=address)
        taxes = []
        for tax in (0.00, 0.05, 0.08, 0.23):
            taxes.append(Tax.create(tax_value=tax))
        for i in range(4):
            Item.create(title='Title {}'.format(i), name='Name {}'.format(i), price=12.34, earnings=11.22,
                        vat=taxes[i])
        self.items = Item.objects.all()
        self.marketplace = Marketplace()
        self.marketplace.save()
        self.transaction = Transaction.create(vendor=self.company, customer=self.customer, marketplace=self.marketplace,
                                              country_code='PL')
        for item in Item.objects.all():
            self.transaction.items.add(SoldItem.create(item=item, units=10))
        self.receipt = Receipt.create(transaction=self.transaction)
        self.invoice = Invoice.create(receipt=self.receipt)
        self.invoice.end_invoice()

    def test_generate_sales_report(self):
        date = datetime.now()
        request = self.factory.get('generate_sales_report')
        response = self.view(request, year=date.year, month=date.month)
        self.assertEqual(response.status_code, 200)

    def test_generate_sales_report_without_invoices(self):
        self.invoice.delete()
        date = datetime.now()
        request = self.factory.get('generate_sales_report')
        response = self.view(request, year=date.year, month=date.month)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'no receipts in selected month')

    def test_generate_sales_report_with_wrong_month_value(self):
        date = datetime.now()
        request = self.factory.get('generate_sales_report')
        response = self.view(request, year=date.year, month=13)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'month_error')

        request = self.factory.get('generate_sales_report')
        response = self.view(request, year=date.year, month=0)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'month_error')

        request = self.factory.get('generate_sales_report')
        response = self.view(request, year=date.year, month=-1)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'month_error')

        request = self.factory.get('generate_sales_report')
        response = self.view(request, year=date.year, month=1.1)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'month_error')

        request = self.factory.get('generate_sales_report')
        response = self.view(request, year=date.year, month=-1.1)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'month_error')

        request = self.factory.get('generate_sales_report')
        response = self.view(request, year=date.year, month=True)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'month_error')

        request = self.factory.get('generate_sales_report')
        response = self.view(request, year=date.year, month=False)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'month_error')

        request = self.factory.get('generate_sales_report')
        response = self.view(request, year=date.year, month=None)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'month_error')

        request = self.factory.get('generate_sales_report')
        response = self.view(request, year=date.year, month=list())
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'month_error')

        request = self.factory.get('generate_sales_report')
        response = self.view(request, year=date.year, month=tuple())
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'month_error')

        request = self.factory.get('generate_sales_report')
        response = self.view(request, year=date.year, month=dict())
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'month_error')

        request = self.factory.get('generate_sales_report')
        response = self.view(request, year=date.year, month=set())
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'month_error')

    def test_generate_sales_report_with_wrong_year(self):
        date = datetime.now()
        request = self.factory.get('generate_sales_report')
        response = self.view(request, year=date.year + 1, month=date.month)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'year error')

        request = self.factory.get('generate_sales_report')
        response = self.view(request, year=1900, month=date.month)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'year error')

        request = self.factory.get('generate_sales_report')
        response = self.view(request, year=date.year + 0.5, month=date.month)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'year error')

        request = self.factory.get('generate_sales_report')
        response = self.view(request, year=0, month=date.month)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'year error')

        request = self.factory.get('generate_sales_report')
        response = self.view(request, year=-1, month=date.month)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'year error')

        request = self.factory.get('generate_sales_report')
        response = self.view(request, year=1.1, month=date.month)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'year error')

        request = self.factory.get('generate_sales_report')
        response = self.view(request, year=-1.1, month=date.month)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'year error')

        request = self.factory.get('generate_sales_report')
        response = self.view(request, year=True, month=date.month)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'year error')

        request = self.factory.get('generate_sales_report')
        response = self.view(request, year=False, month=date.month)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'year error')

        request = self.factory.get('generate_sales_report')
        response = self.view(request, year=None, month=date.month)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'year error')

        request = self.factory.get('generate_sales_report')
        response = self.view(request, year=list(), month=date.month)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'year error')

        request = self.factory.get('generate_sales_report')
        response = self.view(request, year=tuple(), month=date.month)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'year error')

        request = self.factory.get('generate_sales_report')
        response = self.view(request, year=dict(), month=date.month)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'year error')

        request = self.factory.get('generate_sales_report')
        response = self.view(request, year=set(), month=date.month)
        self.assertEqual(response.data['status'], 'ERROR')
        self.assertEqual(response.data['message'], 'year error')
