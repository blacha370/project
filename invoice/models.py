from django.db import models


class Address(models.Model):
    country = models.CharField(max_length=50, null=False)
    city = models.CharField(max_length=100, null=False)
    street = models.CharField(max_length=100, null=False)
    building_number = models.PositiveSmallIntegerField()
    apartment_number = models.PositiveSmallIntegerField()


class Company(models.Model):
    name = models.CharField(max_length=100, null=False)
    SKU = models.CharField(max_length=100, null=False)
    address = models.OneToOneField('Address', on_delete=models.CASCADE)


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
    category = models.PositiveSmallIntegerField(choices=CATEGORIES, default=2)
    earnings = models.PositiveSmallIntegerField()
    subscription_term = models.PositiveSmallIntegerField(choices=SUBSCRIPTION_TERMS, default=None)


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
