from django.db import models
from django.utils.crypto import get_random_string


class Address(models.Model):
    country = models.CharField(max_length=50, null=False)
    city = models.CharField(max_length=100, null=False)
    postal_code = models.CharField(max_length=6, null=False)
    street = models.CharField(max_length=100, null=False)
    building_number = models.PositiveSmallIntegerField()
    apartment_number = models.PositiveSmallIntegerField()


class Company(models.Model):
    name = models.CharField(max_length=100, null=False)
    SKU = models.CharField(max_length=150, null=False)
    address = models.OneToOneField('Address', on_delete=models.CASCADE)

    @classmethod
    def _generate_SKU(cls):
        SKU = get_random_string(length=150)
        if cls.objects.filter(SKU=SKU):
            SKU = get_random_string(length=150)
        return SKU


class Customer(models.Model):
    name = models.CharField(max_length=100, null=False)
    address = models.ForeignKey('Address', on_delete=models.CASCADE)
    app_id = models.CharField(max_length=100)


class Marketplace(models.Model):
    name = models.CharField(max_length=50, null=False, default='amazon.com')
    currency = models.CharField(max_length=3, null=False, default='USD')


class Item(models.Model):
    CATEGORIES = (
        (1, 'subscription'),
        (2, 'application'),
        (3, 'in_app'),
        (4, 'game'),
        (5, 'in_game')
    )
    SUBSCRIPTION_TERMS = (
        (1, 'weekly'),
        (2, 'biweekly'),
        (3, 'monthly'),
        (4, 'bimonthly'),
        (5, 'quarterly'),
        (6, 'semi-annually'),
        (7, 'annually')
    )
    ASIN = models.CharField(max_length=10, null=False)
    title = models.CharField(max_length=50, null=False)
    name = models.CharField(max_length=50, null=False)
    price = models.PositiveSmallIntegerField()
    category = models.PositiveSmallIntegerField(choices=CATEGORIES, null=True)
    earnings = models.PositiveSmallIntegerField()
    subscription_term = models.PositiveSmallIntegerField(choices=SUBSCRIPTION_TERMS, default=None, null=True)
    vat = models.PositiveSmallIntegerField(default=0.23)

    @classmethod
    def _validate_data(cls, title, name, price, earnings, category, subscription_term, vat):
        messages = []
        if not isinstance(title, str) or len(str(title)) > 50:
            messages.append('Title error')
        if not isinstance(name, str) or len(str(name)) > 50:
            messages.append('Name error')
        if not isinstance(price, (int, float)) or isinstance(price, bool) or price <= 0:
            messages.append('Price error')
        if not(isinstance(earnings, (int, float))) or isinstance(earnings, bool) or earnings <= 0 or earnings > price:
            messages.append('Earnings error')
        if not isinstance(category, (int, type(None))) or isinstance(category, bool):
            messages.append('Category error')
        if not isinstance(subscription_term, (int, type(None))) or isinstance(subscription_term, bool):
            messages.append('Subscription term error')
        if not isinstance(vat, (int, float)) or isinstance(vat, bool):
            messages.append('Vat error')
        if messages:
            raise TypeError(messages)
        else:
            return True

    @classmethod
    def _generate_asin(cls):
        asin = get_random_string(length=10)
        if cls.objects.filter(ASIN=asin):
            asin = get_random_string(length=10)
        return asin

    @classmethod
    def create(cls, title: str, name: str, price: int, earnings: int, category: int = None,
               subscription_term: int = None, vat: int = 0.23):
        cls._validate_data(title, name, price, earnings, category, subscription_term, vat)
        asin = cls._generate_asin()
        instance = cls(ASIN=asin, title=title, name=name, price=price, earnings=earnings, category=category,
                       subscription_term=subscription_term, vat=vat)
        instance.save()
        return instance


class SoldItem(models.Model):
    item = models.ForeignKey('Item', on_delete=models.CASCADE)
    units = models.PositiveSmallIntegerField()
    trial = models.BooleanField(null=True)


class Transaction(models.Model):
    vendor = models.ForeignKey('Company', on_delete=models.CASCADE, null=False)
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE, null=False)
    items = models.ManyToManyField('SoldItem')
    country_code = models.CharField(max_length=2, null=False)
    refund = models.BooleanField(default=False)
    adjustment = models.BooleanField(default=False)
    time = models.DateTimeField(auto_now_add=True)


class Receipt(models.Model):
    transaction = models.OneToOneField('Transaction', on_delete=models.CASCADE)
    receipt_id = models.CharField(max_length=20, unique=True)
    time = models.DateTimeField(auto_now_add=True)


class Invoice(models.Model):
    receipt = models.OneToOneField('Receipt', on_delete=models.CASCADE)
    invoice_id = models.CharField(max_length=20, unique=True)
    ended = models.BooleanField(default=False)
    time = models.DateTimeField(default=None)


class AdvanceInvoice(models.Model):
    invoice = models.ForeignKey('Invoice', on_delete=models.CASCADE)
    payment = models.SmallIntegerField()
    advance_invoice_id = models.CharField(max_length=20, unique=True)
    time = models.DateTimeField(auto_now_add=True)
