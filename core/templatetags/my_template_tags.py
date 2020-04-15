from django import template
from core.models import Order

register = template.Library()


@register.simple_tag
def define(val=None):
    return val


@register.filter
def cart_item_count(user):
    if user.is_authenticated:
        qs = Order.objects.filter(user=user, is_ordered=False)
        if qs.exists():
            return qs[0].order_items.count()
    return 0


country_id = None


@register.filter
def set_country_id(country):
    country_id = country.id
    return
