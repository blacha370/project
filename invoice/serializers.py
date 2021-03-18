from rest_framework.serializers import HyperlinkedModelSerializer
from rest_framework.fields import ReadOnlyField
from .models import Address, Company, Customer, Marketplace, Tax, Item, SoldItem, Transaction, Receipt, Invoice,\
    AdvanceInvoice


class AddressSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Address
        fields = ['url', 'country', 'city', 'postal_code', 'street', 'building_number', 'apartment_number']


class CompanySerializer(HyperlinkedModelSerializer):
    address = AddressSerializer(many=False)

    class Meta:
        model = Company
        fields = ['url', 'name', 'SKU', 'address']


class CustomerSerializer(HyperlinkedModelSerializer):
    address = AddressSerializer(many=False)

    class Meta:
        model = Customer
        fields = ['url', 'name', 'app_id', 'address']


class MarketplaceSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Marketplace
        fields = ['url', 'name', 'currency']


class TaxSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Tax
        fields = ['url', 'tax_name', 'tax_value']


class ItemSerializer(HyperlinkedModelSerializer):
    vat = TaxSerializer(many=False)

    class Meta:
        model = Item
        fields = ['url', 'ASIN', 'title', 'name', 'price', 'category', 'earnings', 'subscription_term', 'vat']


class SoldItemSerializer(HyperlinkedModelSerializer):
    item = ItemSerializer(many=False)
    net_value = ReadOnlyField()
    vat_value = ReadOnlyField()
    total_value = ReadOnlyField()
    total_earnings = ReadOnlyField()

    class Meta:
        model = SoldItem
        read_only = ['net_value', 'vat_value', 'total_value', 'total_earnings']
        fields = ['url', 'item', 'units', 'trial', 'net_value', 'vat_value', 'total_value', 'total_earnings']


class TransactionSerializer(HyperlinkedModelSerializer):
    vendor = CompanySerializer(many=False)
    customer = CustomerSerializer(many=False)
    marketplace = MarketplaceSerializer(many=False)
    items = SoldItemSerializer(many=True)
    net_value = ReadOnlyField()
    tax_values = ReadOnlyField()
    tax_value = ReadOnlyField()
    total_value = ReadOnlyField()
    total_earnings = ReadOnlyField()

    class Meta:
        model = Transaction
        read_only = ['net_value', 'tax_values', 'tax_value', 'total_value', 'total_earnings']
        fields = ['url', 'vendor', 'customer', 'marketplace', 'transaction_id', 'items', 'country_code', 'refund',
                  'adjustment', 'time', 'net_value', 'tax_values', 'tax_value', 'total_value', 'total_earnings']


class ReceiptSerializer(HyperlinkedModelSerializer):
    transaction = TransactionSerializer(many=False)

    class Meta:
        model = Receipt
        fields = ['url', 'transaction', 'receipt_id', 'time']


class InvoiceSerializer(HyperlinkedModelSerializer):
    receipt = ReceiptSerializer(many=False)

    class Meta:
        model = Invoice
        fields = ['url', 'receipt', 'invoice_id', 'ended', 'time']


class AdvanceInvoiceSerializer(HyperlinkedModelSerializer):
    invoice = InvoiceSerializer(many=False)

    class Meta:
        model = AdvanceInvoice
        fields = ['url', 'invoice', 'payment', 'advance_invoice_id', 'time']
