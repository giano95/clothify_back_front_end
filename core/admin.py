from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from core.models import (
    User,
    CheckoutInfo,
)


admin.site.register(User, UserAdmin)
admin.site.register(CheckoutInfo)
