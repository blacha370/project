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

