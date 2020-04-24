from django.urls import path
from .views import (
    # HomeView,
    ItemView,
    OrderSummaryView,
    CheckoutView,
    PaymentView,
    add_to_cart,
    update_cart,
    secret,
    get_oauth_url,
    handle_oauth_redirect,
    get_countries,
    get_regions,
    get_cities,
    add_post,
    tmp,
    items_view
)


app_name = 'core'
urlpatterns = [
    path('', items_view, name='home'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('item/<pk>/', ItemView.as_view(), name='item'),
    path('order_summary/', OrderSummaryView.as_view(), name='order_summary'),
    path('add_to_cart/<pk>/', add_to_cart, name='add_to_cart'),
    path('update_cart/<pk>/<q>/', update_cart, name='update_cart'),
    path('payment/<payment_option>/', PaymentView.as_view(), name='payment'),
    path('secret/', secret, name='secret'),
    path('connect/get_oauth_url/', get_oauth_url, name='get_oauth_url'),
    path('connect/oauth/', handle_oauth_redirect, name='handle_oauth_redirect'),
    path('get_countries/', get_countries, name='get_countries'),
    path('get_regions/', get_regions, name='get_regions'),
    path('get_cities/', get_cities, name='get_cities'),
    path('add_post/', add_post, name='add_post'),
    path('tmp/', tmp, name='tmp'),
]
