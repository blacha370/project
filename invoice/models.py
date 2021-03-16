from django.db import models
from django.utils.crypto import get_random_string
from django.utils import timezone


class Address(models.Model):
    country = models.CharField(max_length=50, null=False)
    city = models.CharField(max_length=100, null=False)
    postal_code = models.CharField(max_length=6, null=False)
    street = models.CharField(max_length=100, null=False)
    building_number = models.PositiveSmallIntegerField()
    apartment_number = models.PositiveSmallIntegerField(null=True, default=None)

    @classmethod
    def _validate_data(cls, country, city, postal_code, street, building_number, apartment_number):
        messages = []
        if not isinstance(country, str) or len(country) > cls.country.field.max_length or \
                country.replace(' ', '') == '':
            messages.append('Country error')
        if not isinstance(city, str) or len(city) > cls.city.field.max_length or city.replace(' ', '') == '':
            messages.append('City error')
        if not isinstance(postal_code, str) or len(postal_code) > cls.postal_code.field.max_length or \
                postal_code.replace(' ', '') == '':
            messages.append('Postal code error')
        if not isinstance(street, str) or len(street) > cls.street.field.max_length or street.replace(' ', '') == '':
            messages.append('Street error')
        if not isinstance(building_number, int) or isinstance(building_number, bool) or int(building_number) <= 0:
            messages.append('Building number error')
        if apartment_number is not None:
            if not isinstance(apartment_number, int) or isinstance(apartment_number, bool) or apartment_number <= 0:
                messages.append('Apartment number error')
        if messages:
            raise TypeError
        else:
            return True

    @classmethod
    def create(cls, country: str, city: str, postal_code: str, street: str, building_number: int,
               apartment_number: int = None):
        cls._validate_data(country=country, city=city, postal_code=postal_code, street=street,
                           building_number=building_number, apartment_number=apartment_number)
        instance = cls(country=country, city=city, postal_code=postal_code, street=street,
                       building_number=building_number, apartment_number=apartment_number)
        instance.save()
        return instance

    def __str__(self):
        first_line = self.street + ' ' + str(self.building_number)
        if self.apartment_number:
            first_line += ' ' + str(self.apartment_number)
        first_line += '\n'
        second_line = self.postal_code + ' ' + self.city + '\n'
        third_line = self.country
        return first_line + second_line + third_line


class Company(models.Model):
    name = models.CharField(max_length=100, null=False, unique=True)
    SKU = models.CharField(max_length=150, null=False, unique=True)
    address = models.OneToOneField('Address', on_delete=models.CASCADE, unique=True)

    @classmethod
    def _validate_data(cls, name, address):
        messages = []
        if not isinstance(name, str) or len(name) > cls.name.field.max_length or cls.objects.filter(name=name) or \
                name.replace(' ', '') == '':
            messages.append('Name error')
        if not isinstance(address, Address) or cls.objects.filter(address=address):
            messages.append('Address error')
        if messages:
            raise TypeError(messages)
        else:
            return True

    @classmethod
    def _generate_SKU(cls):
        SKU = get_random_string(length=150)
        if cls.objects.filter(SKU=SKU):
            SKU = get_random_string(length=150)
        return SKU

    @classmethod
    def create(cls, name, address):
        cls._validate_data(name=name, address=address)
        SKU = cls._generate_SKU()
        instance = cls(name=name, address=address, SKU=SKU)
        instance.save()
        return instance


class Customer(models.Model):
    name = models.CharField(max_length=100, null=False)
    address = models.ForeignKey('Address', on_delete=models.CASCADE)
    app_id = models.CharField(max_length=100, unique=True)

    @classmethod
    def _validate_data(cls, name, address):
        messages = []
        if not isinstance(name, str) or len(name) > cls.name.field.max_length or name.replace(' ', '') == '':
            messages.append('Name error')
        if not isinstance(address, Address):
            messages.append('Address error')
        if messages:
            raise TypeError(messages)
        else:
            return True

    @classmethod
    def _generate_app_id(cls):
        app_id = get_random_string(length=100)
        if cls.objects.filter(app_id=app_id):
            app_id = get_random_string(length=100)
        return app_id

    @classmethod
    def create(cls, name: str, address: Address):
        cls._validate_data(name=name, address=address)
        app_id = cls._generate_app_id()
        instance = cls(name=name, address=address, app_id=app_id)
        instance.save()
        return instance


class Marketplace(models.Model):
    name = models.CharField(max_length=50, null=False, default='amazon.com')
    currency = models.CharField(max_length=3, null=False, default='USD')


class Tax(models.Model):
    tax_value = models.DecimalField(unique=True, decimal_places=2, max_digits=3)
    tax_name = models.CharField(max_length=8, unique=True)

    @classmethod
    def create(cls, tax_value: float):
        if not isinstance(tax_value, float) or tax_value < 0 or tax_value >= 1:
            raise TypeError('Tax value error: tax_value should be float greater on equal to 0 and lower than 1')
        tax_name = 'Vat_' + '{}'.format(round(tax_value, 2))
        instance = cls(tax_value=tax_value, tax_name=tax_name)
        instance.save()
        return instance


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
    vat = models.ForeignKey('Tax', on_delete=models.CASCADE)

    @classmethod
    def _validate_data(cls, title, name, price, earnings, category, subscription_term, vat):
        messages = []
        if not isinstance(title, str) or len(title) > cls.title.field.max_length:
            messages.append('Title error')
        if not isinstance(name, str) or len(name) > cls.name.field.max_length:
            messages.append('Name error')
        if not isinstance(price, (int, float)) or isinstance(price, bool) or price <= 0:
            messages.append('Price error')
        if not(isinstance(earnings, (int, float))) or isinstance(earnings, bool) or earnings <= 0 or earnings > price:
            messages.append('Earnings error')
        if not isinstance(category, (int, type(None))) or isinstance(category, bool):
            messages.append('Category error')
        if not isinstance(subscription_term, (int, type(None))) or isinstance(subscription_term, bool):
            messages.append('Subscription term error')
        if not isinstance(vat, Tax):
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
    def create(cls, title: str, name: str, price: int, earnings: int, vat: Tax, category: int = None,
               subscription_term: int = None):
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

    @classmethod
    def _validate_data(cls, item, units, trial):
        messages = []
        if not isinstance(item, Item):
            messages.append('Item error')
        if not isinstance(units, int) or isinstance(units, bool):
            messages.append('Units error')
        if not isinstance(trial, bool) and trial is not None:
            messages.append('Trial error')
        if messages:
            raise TypeError(messages)
        else:
            return True

    @classmethod
    def create(cls, item: Item, units: int, trial: bool = None):
        cls._validate_data(item, units, trial)
        instance = cls(item=item, units=units, trial=trial)
        instance.save()
        return instance

    @property
    def net_value(self):
        return self.item.price * self.units

    @property
    def vat_value(self):
        return {'name': self.item.vat.tax_name, 'value': self.item.price * self.item.vat.tax_value * self.units}

    @property
    def total_value(self):
        return self.net_value + self.vat_value

    @property
    def total_earnings(self):
        return self.item.earnings * self.units


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
