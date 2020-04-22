from django.db import models
from django.conf import settings
from django.shortcuts import reverse
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.exceptions import ObjectDoesNotExist
from picklefield.fields import PickledObjectField
from django.contrib.auth.models import AbstractUser


LOREM_IPSUM = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris id turpis porttitor, vestibulum massa vel, tristique ante. Curabitur hendrerit quam massa, sit amet lobortis tellus consectetur eu. Suspendisse aliquet commodo tristique. Vivamus maximus pharetra sapien, ornare tempor libero egestas sed. Phasellus massa magna, tincidunt vitae nisl eget, rhoncus bibendum enim. Duis sed lectus sed leo pharetra ultrices id sit amet dolor. Vivamus pellentesque mi sed dignissim rhoncus. Nunc in sollicitudin quam. Nullam ornare dui quis sapien bibendum, nec sagittis purus venenatis.'
DEFAULT_IMG = 'https://mdbootstrap.com/img/Photos/Horizontal/E-commerce/Vertical/15.jpg'

CATEGORY_CHOICES = (
    ('S', 'Shirts'),
    ('SW', 'Sport Wears'),
    ('O', 'Outwears'),
    ('A', 'Accessories'),
    ('CW', 'Casual Wears')
)

LABEL_COLOR_CHOICES = (
    ('P', 'primary-color'),
    ('S', 'secondary-color'),
    ('D', 'danger-color')
)

UNIT_CHOICES = (
    ('stock', 'STOCK'),
    ('each', 'EACH'),
)


class User(AbstractUser):
    TYPE_CHOICES = (
        ('Buyer', 'Buyer'),
        ('Seller', 'Seller')
    )

    user_type = models.CharField(
        choices=TYPE_CHOICES, max_length=10)
    connected_account_id = models.TextField(blank=True, null=True)

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


class PostManager(models.Manager):
    def search(self, **kwargs):
        qs = super().get_queryset()

        # TODO:
        # Split query into words, case insensitive search each field:
        # owner name, title, body, tags, location

        if 'query' in kwargs:
            query = kwargs['query']
            qs = qs.filter(Q(title__icontains=query)
                           | Q(body__icontains=query))

        if 'tags' in kwargs:
            tags = kwargs['tags']
            # Filter to posts with tags in the provided set
            qs = qs.filter(tags__name__in=tags)

        return qs


class Item(models.Model):
    id = models.AutoField(primary_key=True)

    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE, blank=True, null=True)
    objects = PostManager()
    name = models.CharField(max_length=100)
    price = models.FloatField()
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    description = models.CharField(max_length=1000, default=LOREM_IPSUM)
    img = models.ImageField(upload_to='item/img/',
                            blank=True, default=DEFAULT_IMG)
    unit = models.CharField(
        max_length=80, choices=UNIT_CHOICES, default='each')
    discounted_price = models.FloatField(blank=True, null=True)
    label = models.CharField(max_length=25, blank=True, null=True)
    label_color = models.CharField(
        choices=LABEL_COLOR_CHOICES, max_length=1, blank=True, null=True)

    def get_price(self):
        if self.discounted_price:
            return self.discounted_price
        else:
            return self.price

    def get_discount(self):
        if self.discounted_price:
            return self.price - self.discounted_price
        else:
            return 0

    def get_recommended_item(self):
        if self.category:
            return Item.objects.filter(category=self.category).exclude(id=self.id)[:4]
        else:
            return 0

    def get_url(self):
        return reverse('core:item', kwargs={'pk': self.id})

    def get_add_to_cart_url(self):
        return reverse('core:add_to_cart', kwargs={'pk': self.id})

    def __str__(self):
        return self.name


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    is_ordered = models.BooleanField(default=False)
    quantity = models.IntegerField(default=1)

    def get_total_price(self):
        return self.item.get_price() * self.quantity

    def get_total_discount(self):
        return self.item.get_discount() * self.quantity

    def __str__(self):
        return f"{self.quantity} of {self.item.id}"


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    order_items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    is_ordered = models.BooleanField(default=False)
    checkout_info = models.ForeignKey(
        CheckoutInfo, on_delete=models.SET_NULL, null=True, blank=True)

    def get_total_order_price(self):
        total = 0.0
        for order_item in self.order_items.all():
            total += float(order_item.get_total_price())
        return total

    def __str__(self):
        return self.user.username
