from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Item, OrderItem, Order, CheckoutInfo, User


admin.site.register(User, UserAdmin)
admin.site.register(Item)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(CheckoutInfo)
