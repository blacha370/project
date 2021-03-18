from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from .models import (Address, Company, Customer, Marketplace, Tax, Item, SoldItem, Transaction, Receipt, Invoice,
                     AdvanceInvoice)
from .serializers import (AddressSerializer, CompanySerializer, CustomerSerializer, MarketplaceSerializer,
                          TaxSerializer, ItemSerializer, SoldItemSerializer, TransactionSerializer, ReceiptSerializer,
                          InvoiceSerializer, AdvanceInvoiceSerializer)


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
            vat = Tax.objects.get(tax_value=request.data['tax_value'])
            item = Item.create(vat=vat, **item_dict)
            serializer = ItemSerializer(item, many=False, context={'request': request})
            return Response({'status': 'OK', 'item': serializer.data})
        except KeyError as e:
            return Response({'status': 'Erorr', 'message': 'missing argument: tax_value'})
        except Tax.DoesNotExist:
            return Response({'status': 'ERROR', 'message': 'Tax with provided tax_value does not exist'})
        except TypeError as e:
            return Response({'status': 'ERROR', 'message': str(e).replace('create() ', '')})


class CreateTransaction(APIView):
    transaction_keys = ['SKU', 'app_id', 'marketplace_name', 'country_code', 'refund', 'adjustment']
    items_key = 'items'

    def post(self, request):
        items = []
        error_items = []
        try:
            for item in request.data['items']:
                try:
                    if item['count'] <= 0 or not isinstance(item['count'], int) or isinstance(item['count'], bool):
                        error_items.append(item['ASIN'])
                        continue
                    items.append((Item.objects.get(ASIN=item['ASIN']), item['count']))
                except Item.DoesNotExist:
                    error_items.append(item['ASIN'])
                except KeyError:
                    return Response({'status': 'ERROR', 'message': 'item {} does not have count'.format(item['ASIN'])})
        except KeyError:
            return Response({'status': 'ERROR', 'message': 'missing argument: items'})
        if error_items:
            return Response({'status': 'ERROR', 'message': 'items error: {}'.format(', '.join(error_items))})

        transaction_dict = {key: value for key, value in request.data.items() if key in self.transaction_keys}
        try:
            transaction = Transaction.create(**transaction_dict)
            for item in items:
                sold_item = SoldItem.create(item=item[0], units=item[1])
                transaction.items.add(sold_item)
            serializer = TransactionSerializer(transaction, many=False, context={'request': request})
            return Response({'status': 'OK', 'transaction': serializer.data})
        except TypeError as e:
            return Response({'status': 'ERROR', 'message': str(e)})


class CreateReceipt(APIView):
    def post(self, request):
        try:
            transaction = Transaction.objects.get(pk=request.data['transaction_id'])
            receipt = Receipt.create(transaction=transaction)
            serializer = ReceiptSerializer(receipt, many=False, context={'request': request})
            return Response({'status': 'OK', 'receipt': serializer.data})
        except Transaction.DoesNotExist:
            return Response({'status': 'ERROR', 'message': 'Transaction with provided id does not exist'})
        except KeyError:
            return Response({'status': 'Erorr', 'message': 'missing argument: transaction_id'})
        except TypeError as e:
            return Response({'status': 'ERROR', 'message': str(e).replace('create() ', '')})


class CreateInvoice(APIView):
    def post(self, request):
        try:
            receipt = Receipt.objects.get(receipt_it=request.data['receipt_id'])
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
            return Response({'status': 'ERROR', 'message': str(e)})
        except TypeError as e:
            return Response({'status': 'ERROR', 'message': str(e).replace('create() ', '')})

