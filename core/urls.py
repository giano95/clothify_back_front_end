from django.urls import path
from core.views import (
    HomeView,
    ShopView,
    CheckoutView,
    PaymentView,
    ContactView,
    secret,
    get_oauth_url,
    handle_oauth_redirect,
    get_countries,
    get_regions,
    get_cities,
    dummy_url,
)


app_name = 'core'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('shop/', ShopView.as_view(), name="shop"),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('payment/<payment_option>/', PaymentView.as_view(), name='payment'),
    path('contact/', ContactView.as_view(), name="contact"),
    path('secret/', secret, name='secret'),
    path('connect/get_oauth_url/', get_oauth_url, name='get_oauth_url'),
    path('connect/oauth/', handle_oauth_redirect, name='handle_oauth_redirect'),
    path('dummy_url/', dummy_url, name='dummy_url'),
    path('get_countries/', get_countries, name='get_countries'),
    path('get_regions/', get_regions, name='get_regions'),
    path('get_cities/', get_cities, name='get_cities'),
]
