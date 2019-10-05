from django.db import models

from account.models import PaymentMethod
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete

# Create your models here.

class Merchant(models.Model):

    company_name = models.CharField(max_length=100)
    contact_name = models.CharField(max_length=100)
    contact_title = models.CharField(max_length=100)
    phone = models.CharField(max_length=100, blank=True)
    telephone = models.CharField(max_length=100, null=True)
    fax = models.CharField(max_length=100, null=True)
    company_logo = models.CharField(max_length=100, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_methods = models.ManyToManyField(PaymentMethod)
    #can_shipped = models.BooleanField(default=False)

    class Meta:
        db_table = "merchant"
        verbose_name = "Merchant"
        verbose_name_plural = "Merchants"




def merchant_receiver(sender, instance, created, *args, **kwargs):
    if created :
        merchant_profile = Merchant.objects.create(user=instance)

post_save.connect(merchant_receiver,sender=User)
