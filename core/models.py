from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.db.models.signals import post_save, post_delete
from django.shortcuts import reverse
from address.models import (Region, Province, City, Barangay)
from account.models import (UserProfile, Address, PaymentMethod)
from mall.models import Merchant

from django.core.validators import MaxValueValidator, MinValueValidator

CONDITION = (
    ('N', 'New'),
    ('U', 'Used (like new)'),
)

PROVIDER = (
    ('Visa', 'Visa'),
    ('MasterCard', 'MasterCard'),

)

CARD_TYPE = (
    ('debit', 'Debit Card'),
    ('credit', 'Credit Card'),
    ('prepaid', 'Prepaid Card'),
)

MONTH = (
    ('01', 'January'), #Jan
    ('02', 'February'), #Feb
    ('03', 'MARCH'), #
    ('04', 'APRIL'), #
    ('05', 'MAY'), #May
    ('06', 'JUNE'), #Jun
    ('07', 'JULY'), #Jul
    ('08', 'AUGUST'), #Aug
    ('09', 'SEPTEMBER'), #Sep
    ('10', 'OCTOBER'), #Oct
    ('11', 'NOVEMBER'), #Nov
    ('12', 'DECEMBER'), #Dec
)

PACKAGE_HANDLING = (
    ('none', 'Dry Goods Only'),
    ('fragile', 'Fragile'),
    ('liquid', 'Liquid'),
    ('others', 'Batteries/Powerbanks, etc.'),
)

PAYMENT_OPTIONS = (
    ('card','Debit/Credit Card'),
    ('paypal','Paypal'),
    ('dragon pay', 'Dragon Pay'),
)

class Category(models.Model):

    category_name = models.CharField(max_length=100)
    description = models.TextField()
    logo = models.ImageField()
    status = models.BooleanField(default=True)
    slug = models.SlugField()

    def __str__(self):
        return self.category_name

    def get_absolute_url(self):
        return reverse("core:category-detail", kwargs= {'slug': self.slug})

    class Meta:
        db_table = "category"
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class Product(models.Model):

    product_name = models.CharField(max_length=100)
    product_description = models.TextField()
    product_price = models.FloatField(validators=[MinValueValidator(9.00), MaxValueValidator(999999)])
    product_stock = models.IntegerField(default=1)
    product_image = models.ImageField()
    product_SKU = models.TextField()
    slug = models.SlugField()
    product_code = models.CharField(max_length=254)

    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    #variation = models.ForeignKey() # Color, Size
    weight = models.FloatField()
    condition = models.CharField(choices=CONDITION, max_length=1)
    published_product = models.BooleanField(default=True)
    discount_price = models.FloatField(null=True)
    rating = models.IntegerField(default=0)
    reward_points = models.FloatField(default=0.0)

    on_sale = models.BooleanField(default=False)
    sale_price = models.FloatField()

    #wholesale = models.
        # Min Order - Max Order : Unit Price

    #packaging_size =
        # Width (in cm), Length (in cm), Height (in cm)

    #shipping fee
        #

    def __str__(self):
        return self.product_name

    def get_absolute_url(self):
        return reverse("", kwargs= {'slug': self.slug})

    def get_add_to_cart_url(self):

        return reverse("", kwargs={'slug': self.slug})

    def get_remove_from_cart_url(self):
        return reverse("", kwargs={'slug': self.slug})

    class Meta:

        db_table = "product"
        verbose_name = "Product"
        verbose_name_plural = "Products"


class ProductImage(models.Model):

    filename = models.ImageField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    class Meta:
        db_table = "ProductImage"
        verbose_name = "Product Image"
        verbose_name_plural = "Product Images"


class Variation(models.Model):

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    color = models.CharField(null=True, max_length=100)
    size_kg = models.FloatField(null=True)

    class Meta:
        db_table = "variation"
        verbose_name = "Variation"
        verbose_name_plural = "Variations"


class OrderDetail(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    in_cart = models.BooleanField(default=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return "{} of {}".format(self.quantity, self.product.product_name)

    def get_total_item_price(self):
        return self.quantity * self.product.product_price

    def get_total_discount_item_prioe(self):
        return self.quantity * self.product.discount_price

    def get_amount_saved(self):

        return self.get_total_item_price() - self.get_total_discount_item_prioe()

    def get_total_price(self):
        if self.product.discount_price:
            return self.get_total_discount_item_prioe()

        return self.get_total_item_price()


    #product =
    class Meta:
        db_table = "order_detail"
        verbose_name = "Order Detail"
        verbose_name_plural = "Order Details"


class Voucher(models.Model):

    voucher_code = models.CharField(max_length=15)
    amount = models.FloatField()
    merchant = models.ForeignKey(User, on_delete=models.CASCADE)
    valid_until = models.DateTimeField()

    def __str__(self):
        return self.voucher_code

    class Meta:
        db_table = "voucher"
        verbose_name = "Voucher"
        verbose_name_plural = "Vouchers"



class Cart(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=1)
    processed = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)

    def get_product_price(self):
        return self.items.product_price * self.quantity

    def __str__(self):
        return self.user.username

    def get_count(self):

        return self.quantity

    class Meta:
        db_table = "cart"
        verbose_name = "Cart"
        verbose_name_plural = "Cart"

#class LogisticRate(models.Model):

#    shipping_fee = models.FloatField(default=80)
#    fee_name = models.CharField()
#    ship_fee_discount = models.FloatField(default=0.0)


#class Logistic(models.Model):

#    company_name = models.CharField(max_length=100)
#    shipping_rates = models.ManyToManyField(LogisticRate)
#    representative_name = models.CharField(max_length=100)
#    representative_email = models.CharField(max_length=100)

#    def __str__(self):
#        return self.company_name

#    class Meta:
#        db_table = "logistic"

class Order(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ref_code = models.CharField(max_length=32, blank=True, null=True)
    cart = models.ManyToManyField(OrderDetail)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    shipping_address = models.ForeignKey(Address, related_name='shipping_address', on_delete=models.SET_NULL, blank=True, null=True)
    billing_address = models.ForeignKey(Address, related_name='billing_address', on_delete=models.SET_NULL,
                                         blank=True, null=True)
    payment_type = models.CharField(choices=PAYMENT_OPTIONS, max_length=32)

    voucher = models.ForeignKey(Voucher, on_delete=models.SET_NULL, blank=True, null=True)
    package_handling = models.CharField(choices=PACKAGE_HANDLING, max_length=100)
    earn_point = models.FloatField(default=0)
    redeem_point = models.FloatField(default=0)

    canceled = models.BooleanField(default=False)
    shipped = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)
    #insured = models.BooleanField()
    #logistic = models.CharField

    def __str__(self):
        return self.user.username

    def set_total_point(self):

        total_point = 0.0

        for product_order in self.cart.all():
            total_point += product_order.product.reward_points

        self.earn_point = total_point

        return total_point

    def transfer_reward(self):
        userdata = UserProfile.objects.filter(user__id=self.request.user.id)
        userdata.loyalty_point = userdata.loyalty_point + self.earn_point
        userdata.save()

    def get_total(self):

        total = 0.0

        for product_order in self.cart.all():
            total += product_order.get_total_price()

        if self.voucher :
            total -= self.voucher.amount

        total_VAT = total * .12

        total = (total + total_VAT) - self.redeem_point

        return total

    def can_transact(self):
        if  self.get_total() > 499 :
            return True
        return False

    class Meta:
        db_table = "Order"
        verbose_name = "Order"
        verbose_name_plural = "Orders"


class CreditCard(models.Model):

    card_no = models.CharField(max_length=32)
    #provider = models.CharField(choices="", max_length=100)
    card_type = models.CharField(choices=CARD_TYPE, max_length=6)
    exp_month = models.CharField(choices=MONTH, max_length=4)
    exp_year = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    deleted = models.BooleanField(default=False)

    class Meta:
        db_table = "card_detail"
        verbose_name = "Card Detail"
        verbose_name_plural = "Card Details"


#class PaymentOption(models.Model):

class Payment(models.Model):

    transact_id = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

    class Meta:
        db_table = "Payment"
        verbose_name = "Payment"
        verbose_name_plural="Payments"


class Refund(models.Model):

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    reason = models.TextField()
    approved = models.BooleanField(default=False)
    email = models.EmailField()

    def __str__(self):
        return "{}".format(self.pk)

    class Meta:
        db_table = "Refund"
        verbose_name = "Refund"
        verbose_name_plural="Refunds"


#def userprofile_receiver(sender, instance, created, *args, **kwargs):
#    if created :
#        userprofile = UserProfile.objects.create(user=instance)

#post_save.connect(userprofile_receiver,sender=User)
