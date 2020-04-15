from django.urls import path
from .views import (
    HomeView,
    ItemView,
    OrderSummaryView,
    CheckoutView,
    add_to_cart,
    update_cart,
)


app_name = 'core'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('item/<pk>/', ItemView.as_view(), name='item'),
    path('order_summary/', OrderSummaryView.as_view(), name='order_summary'),
    path('add_to_cart/<pk>/', add_to_cart, name='add_to_cart'),
    path('update_cart/<pk>/<q>/', update_cart, name='update_cart'),
]
