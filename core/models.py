from django.db import models
from django.conf import settings
from django.shortcuts import reverse

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


class Item(models.Model):
    # Required fields
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    price = models.FloatField()
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    description = models.CharField(max_length=1000, default=LOREM_IPSUM)
    img = models.CharField(max_length=100, default=DEFAULT_IMG)

    # Optional fields
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

    def get_total_order_price(self):
        total = 0
        for order_item in self.order_items.all():
            total += order_item.get_total_price()
        return total

    def __str__(self):
        return self.user.username
