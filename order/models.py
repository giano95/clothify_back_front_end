from django.db import models
from django.conf import settings

from django.db.models.query import QuerySet





class OrderItem(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    item = models.ForeignKey('item.Item', on_delete=models.CASCADE)
    item_size = models.ForeignKey(
        'item.ItemSize', on_delete=models.CASCADE, default=None)
    is_ordered = models.BooleanField(default=False)
    pending = models.BooleanField(default=False)
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
    ordered_date = models.DateTimeField(blank=True, null=True)
    is_ordered = models.BooleanField(default=False)
    checkout_info = models.ForeignKey(
        'core.CheckoutInfo', on_delete=models.SET_NULL, null=True, blank=True)

    def get_total_order_price(self):
        total = 0.0
        for order_item in self.order_items.all():
            total += float(order_item.get_total_price())
        return total

    def empty(self):
        if self.get_total_order_price() == 0:
            return True
        elif not self.order_items:
            return True
        else:
            return False

    def __str__(self):
        return self.user.username + ' order'
