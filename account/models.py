from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from address.models import *
from django.db.models.signals import post_save, post_delete

from django.dispatch import  receiver

ADDRESS_CHOICES = (
    ('B', 'Billing Address'),
    ('S', 'Shipping Address'),
)

GENDER = (
    ('M', 'Male'),
    ('F', 'Female'),
    ('C', 'Custom'),
)

class UserProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=13)
    gender = models.CharField(choices=GENDER, max_length=1)
    birthdate = models.DateField(blank=True)
    loyalty_point = models.FloatField(default=0)

    def __str__(self):
        return self.user.username

    def get_total_points(self):
        return self.loyalty_point

    class Meta:
        db_table = "auth_user_profile"
        verbose_name = "Customer Account"
        verbose_name_plural = "Customers Account"
    
class Address(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    consignee = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=13)

    landmark = models.CharField(max_length=100)
    detailed_address = models.CharField(max_length=100)
    barangay = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    province = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=4)

    address_type = models.CharField(choices=ADDRESS_CHOICES, max_length=1)
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def get_exact_address(self):
        return f"{self.detailed_address}, {self.barangay}, {self.city}, {self.region}, {self.province} {self.zip_code}"

    class Meta:

        verbose_name_plural = "Customers Address"
        db_table = "address"

class PaymentMethod(models.Model):

    payment_type = models.CharField(max_length=100)
    payment_name = models.CharField(max_length=100)
    status = models.BooleanField(default=True)

    class Meta:
        db_table = "PaymentMethod"


class RoyaltyBonus(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transact_date = models.DateTimeField(auto_now_add=True)
    coin_earn = models.FloatField(default=0)

    class Meta:
        db_table = "royalty_bonus"
        verbose_name = "Royalty Bonus"

class UserVoucher(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    voucher_code = models.CharField(max_length=15)

    used_voucher = models.BooleanField(blank=True,null=True)
    expired_voucher = models.BooleanField(blank=True, null=True)

    valid_voucher = models.BooleanField()

    class Meta:
        db_table = "user_voucher"
        verbose_name = "User Voucher"
        verbose_name_plural = "User Voucher"


#def userprofile_receiver(sender, instance=None, created=False, **kwargs):

#    if created :
#        print("\n\n\n\n\n\n\n\n\nSender: {}\nInstance: {}\nCreated: {}\nkwargs: {}\n\n\n\n\n\n".format(sender, instance,created,kwargs['raw']))
#        UserProfile.objects.create(user=instance, birthdate="1992-05-15")
#    print("\n\n\n\n\nUser has been created\n\n\n\n")
#    instance.userprofile.save()
#post_save.connect(userprofile_receiver,sender=User)

#@receiver(post_save, sender=User)
#def save_user_profile(sender, instance, **kwargs):
#    instance.userprofile.save()