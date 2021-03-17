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
        try:
            address = Address.create(**address_dict)
        except TypeError as e:
            print(e)
            return Response({'status': 'ERROR', 'message': str(e).replace('create() ', '')})
        customer_dict = {key: value for key, value in request.data.items() if key in self.customer_keys}
        customer_dict['address'] = address
        try:
            customer = Customer.create(**customer_dict)
        except TypeError as e:
            address.delete()
            return Response({'status': 'ERROR', 'message': str(e).replace('create() ', '')})
        serializer = CustomerSerializer(customer, many=False, context={'request': request})
        return Response({'status': 'OK', 'customer': serializer.data})


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
