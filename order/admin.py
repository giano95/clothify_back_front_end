from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    OrderItem,
    Order,
)


admin.site.register(OrderItem)
admin.site.register(Order)
