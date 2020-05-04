from django.contrib import admin
from item.models import (
    Item,
    ItemCategory,
    ItemReview,
    ItemColor,
    ItemSize,
    ItemQuantitySize,
    ItemLabel,
    ItemImage,
)

admin.site.register(Item)
admin.site.register(ItemCategory)
admin.site.register(ItemReview)
admin.site.register(ItemColor)
admin.site.register(ItemSize)
admin.site.register(ItemQuantitySize)
admin.site.register(ItemLabel)
admin.site.register(ItemImage)
