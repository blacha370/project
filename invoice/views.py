from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from django.http import HttpResponse
from datetime import datetime
from .models import (Address, Company, Customer, Marketplace, Tax, Item, SoldItem, Transaction, Receipt, Invoice,
                     AdvanceInvoice)
from .serializers import (AddressSerializer, CompanySerializer, CustomerSerializer, MarketplaceSerializer,
                          TaxSerializer, ItemSerializer, SoldItemSerializer, TransactionSerializer, ReceiptSerializer,
                          InvoiceSerializer, AdvanceInvoiceSerializer)
from .functions import generate_sales_report


class AddressViewSet(ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    http_method_names = ['get']


class CompanyViewSet(ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    http_method_names = ['get']


class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    http_method_names = ['get']


class MarketplaceViewSet(ModelViewSet):
    queryset = Marketplace.objects.all()
    serializer_class = MarketplaceSerializer
    http_method_names = ['get']


class TaxViewSet(ModelViewSet):
    queryset = Tax.objects.all()
    serializer_class = TaxSerializer
    http_method_names = ['get']


class ItemViewSet(ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    http_method_names = ['get']


class SoldItemViewSet(ModelViewSet):
    queryset = SoldItem.objects.all()
    serializer_class = SoldItemSerializer
    http_method_names = ['get']


class TransactionViewSet(ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    http_method_names = ['get']


class ReceiptViewSet(ModelViewSet):
    queryset = Receipt.objects.all()
    serializer_class = ReceiptSerializer
    http_method_names = ['get']


class InvoiceViewSet(ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    http_method_names = ['get']


class AdvanceInvoiceViewSet(ModelViewSet):
    queryset = AdvanceInvoice.objects.all()
    serializer_class = AdvanceInvoiceSerializer
    http_method_names = ['get']


class AddCustomer(APIView):
    address_keys = ['country', 'city', 'postal_code', 'street', 'building_number', 'apartment_number']
    customer_keys = ['name']

    def post(self, request):
        address_dict = {key: value for key, value in request.data.items() if key in self.address_keys}
        customer_dict = {key: value for key, value in request.data.items() if key in self.customer_keys}
        try:
            if customer := self.check_if_customer_exists(address_dict=address_dict, customer_dict=customer_dict):
                serializer = CustomerSerializer(customer, many=False, context={'request': request})
                return Response({'status': 'OK', 'customer': serializer.data, 'message': 'customer already exists'})
            address = Address.create(**address_dict)
            customer_dict['address'] = address
            customer = Customer.create(**customer_dict)
            serializer = CustomerSerializer(customer, many=False, context={'request': request})
            return Response({'status': 'OK', 'customer': serializer.data})
        except TypeError as e:
            try:
                if isinstance(dict(locals())['address'], Address):
                    dict(locals())['address'].delete()
            except KeyError:
                pass
            return Response({'status': 'ERROR', 'message': str(e).replace('create() ', '')})

    @staticmethod
    def check_if_customer_exists(address_dict, customer_dict):
        try:
            customers = Customer.objects.filter(name=customer_dict['name'])
            addresses = Address.objects.filter(**address_dict)
            for customer in customers:
                if customer.address in addresses:
                    return customer
        except (TypeError, AssertionError, ValueError, KeyError):
            return False
        return False


class CreateTax(APIView):
    field = 'tax_value'

    def post(self, request):
        try:
            value = request.data[self.field]
            tax = Tax.create(tax_value=value)
            serializer = TaxSerializer(tax, many=False, context={'request': request})
            return Response({'status': 'OK', 'tax': serializer.data})
        except KeyError:
            return Response({'status': 'ERROR', 'message': 'missing argument: tax_value'})
        except TypeError as e:
            return Response({'status': 'ERROR', 'message': str(e)})


class CreateItem(APIView):
    fields = ['title', 'name', 'price', 'earnings', 'category', 'subscription_term']

    def post(self, request):
        item_dict = {key: value for key, value in request.data.items() if key in self.fields}
        try:
            if not isinstance(request.data['tax_value'], (int, float)) or isinstance(request.data['tax_value'], bool):
                raise TypeError('Tax_value error')
            vat = Tax.objects.get(_tax_value=request.data['tax_value'])
            item = Item.create(vat=vat, **item_dict)
            serializer = ItemSerializer(item, many=False, context={'request': request})
            return Response({'status': 'OK', 'item': serializer.data})
        except KeyError as e:
            return Response({'status': 'ERROR', 'message': 'missing argument: tax_value'})
        except Tax.DoesNotExist:
            return Response({'status': 'ERROR', 'message': 'Tax with provided tax_value does not exist'})
        except TypeError as e:
            return Response({'status': 'ERROR', 'message': str(e).replace('create() ', '')})


class CreateTransaction(APIView):
    transaction_keys = ['country_code', 'refund', 'adjustment']
    items_key = 'items'

    def post(self, request):
        items = []
        error_items = []
        try:
            if not isinstance(request.data['items'], (list, tuple)) or not request.data['items']:
                return Response({'status': 'ERROR', 'message': 'items should be list of dicts'})
            for item in request.data['items']:
                try:
                    if not isinstance(item['count'], int) or isinstance(item['count'], bool) or  item['count'] <= 0:
                        error_items.append(item['ASIN'])
                        continue
                    items.append((Item.objects.get(ASIN=item['ASIN']), item['count']))
                except Item.DoesNotExist:
                    error_items.append(item['ASIN'])
                except KeyError:
                    return Response({'status': 'ERROR', 'message': 'each item should contain \'ASIN\' and \'count\' keys'})
                except TypeError:
                    return Response({'status': 'ERROR', 'message': 'item should be dict'})
            if error_items:
                return Response({'status': 'ERROR', 'message': 'items error: {}'.format(', '.join(error_items))})
            vendor = Company.objects.get(SKU=request.data['SKU'])
            customer = Customer.objects.get(app_id=request.data['app_id'])
            marketplace = Marketplace.objects.get(name=request.data['marketplace_name'])
            transaction_dict = {key: value for key, value in request.data.items() if key in self.transaction_keys}
            transaction_dict['vendor'] = vendor
            transaction_dict['customer'] = customer
            transaction_dict['marketplace'] = marketplace
            transaction = Transaction.create(**transaction_dict)
            for item in items:
                sold_item = SoldItem.create(item=item[0], units=item[1])
                transaction.items.add(sold_item)
            serializer = TransactionSerializer(transaction, many=False, context={'request': request})
            return Response({'status': 'OK', 'transaction': serializer.data})
        except Company.DoesNotExist:
            return Response({'status': 'ERROR', 'message': 'Company with provided SKU does not exist'})
        except Customer.DoesNotExist:
            return Response({'status': 'ERROR', 'message': 'Customer with provided app_id does not exist'})
        except Marketplace.DoesNotExist:
            return Response({'status': 'ERROR', 'message': 'Marketplace with provided marketplace_name does not exist'})
        except KeyError as e:
            return Response({'status': 'ERROR', 'message': 'missing argument: ' + str(e).replace('\'', '')})
        except TypeError as e:
            return Response({'status': 'ERROR', 'message': str(e).replace('create() ', '')})


class CreateReceipt(APIView):
    def post(self, request):
        try:
            transaction = Transaction.objects.get(transaction_id=request.data['transaction_id'])
            receipt = Receipt.create(transaction=transaction)
            serializer = ReceiptSerializer(receipt, many=False, context={'request': request})
            return Response({'status': 'OK', 'receipt': serializer.data})
        except Transaction.DoesNotExist:
            return Response({'status': 'ERROR', 'message': 'Transaction with provided id does not exist'})
        except KeyError:
            return Response({'status': 'ERROR', 'message': 'missing argument: transaction_id'})
        except TypeError as e:
            return Response({'status': 'ERROR', 'message': str(e).replace('create() ', '')})


class CreateInvoice(APIView):
    def post(self, request):
        try:
            receipt = Receipt.objects.get(receipt_id=request.data['receipt_id'])
            invoice = Invoice.create(receipt=receipt)
            ended = request.data.get('ended', False)
            if isinstance(ended, bool) and ended:
                invoice.end_invoice()
            serializer = InvoiceSerializer(invoice, many=False, context={'request': request})
            return Response({'status': 'OK', 'invoice': serializer.data})
        except Receipt.DoesNotExist:
            return Response({'status': 'ERROR', 'message': 'Receipt with provided receipt_id does not exist'})
        except KeyError:
            return Response({'status': 'ERROR', 'message': 'missing argument: receipt_id'})
        except TypeError as e:
            return Response({'status': 'ERROR', 'message': str(e).replace('create() ', '')})


class CreateAdvanceInvoice(APIView):
    def post(self, request):
        try:
            invoice = Invoice.objects.get(invoice_id=request.data['invoice_id'])
            advance_invoice = AdvanceInvoice.create(invoice, request.data['payment'])
            serializer = AdvanceInvoiceSerializer(advance_invoice, many=False, context={'request': request})
            return Response({'status': 'OK', 'advance_invoice': serializer.data})
        except Invoice.DoesNotExist:
            return Response({'status': 'ERROR', 'message': 'Invoice with provided invoice_id does not exist'})
        except KeyError as e:
            return Response({'status': 'ERROR', 'message': 'missing argument: ' + str(e)})
        except TypeError as e:
            return Response({'status': 'ERROR', 'message': str(e).replace('create() ', '')})


class EndInvoice(APIView):
    def post(self, request):
        try:
            invoice = Invoice.objects.get(invoice_id=request.data['invoice_id'])
            if invoice.ended:
                return Response({'status': 'ERROR', 'message': 'Invoice is already ended'})
            invoice.end_invoice()
            advance_invoices = AdvanceInvoice.objects.filter(invoice=invoice)
            invoice_serializer = InvoiceSerializer(invoice, many=False, context={'request': request})
            if advance_invoices:
                advance_invoices_serializer = AdvanceInvoiceSerializer(advance_invoices, many=True,
                                                                       context={'request': request})
                return Response({'status': 'OK', 'invoice': invoice_serializer.data,
                                 'advance_invoices': advance_invoices_serializer.data})
            return Response({'status': 'OK', 'invoice': invoice_serializer.data})
        except Invoice.DoesNotExist:
            return Response({'status': 'ERROR', 'message': 'Invoice with provided invoice_id does not exist'})
        except KeyError:
            return Response({'status': 'ERROR', 'message': 'missing argument: invoice_id'})


class GenerateSalesReport(APIView):
    def get(self, request, year: int, month: int):
        date = datetime.now()
        if 2000 > year > date.year:
            return Response({'status': 'ERROR', 'message': 'year error'})
        if 1 > month > 12 or (year == date.year and month > date.month):
            return Response({'status': 'ERROR', 'message': 'month_error'})
        invoices = Invoice.objects.filter(time__year=date.year, time__month=date.month)
        if invoices:
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="Sales_report_{}.{}.csv"'.format(month, year)
            df = generate_sales_report(invoices)
            df.to_csv(path_or_buf=response, sep=',', float_format='%.2f', index=False, decimal=".")
            return response
        else:
            return Response({'status': 'ERROR', 'message': 'no receipts in selected month'})
