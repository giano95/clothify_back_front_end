from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    TYPE_CHOICES = (
        ('Buyer', 'Buyer'),
        ('Seller', 'Seller')
    )

    user_type = models.CharField(
        choices=TYPE_CHOICES, max_length=10)
    connected_account_id = models.TextField(blank=True, null=True)

    class Meta:
        permissions = [
            ('Buyer', 'Can use the application on a Buyer level'),
            ('UnsubSeller',
             'Must submit to stripe'),
            ('SubSeller', 'Can use the application on a Seller level')
        ]

    def get_user_type(self):
        return self.user_type


class CheckoutInfo(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    first_name = models.TextField()
    last_name = models.TextField()
    email = models.EmailField()
    first_address = models.TextField()
    billing_address = models.TextField(blank=True, null=True)
    country = models.TextField()
    region = models.TextField()
    city = models.TextField()
    zip_code = models.TextField()

    def __str__(self):
        return self.user.username + 'checkout info'
