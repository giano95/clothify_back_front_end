from django.urls import path
from knox import views as knox_views
from core.views import (
    ContactAPI,
    UserRegistrationAPI,
    UserLoginAPI,
    PostCheckoutInfoAPI,
    PostPaymentAPI,
    PaymentAPI,
    #_____API VIEWS END_____
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
    permission_denied,
    payment_succeeded,
)


app_name = 'core'
urlpatterns = [
    path('api/contact/', ContactAPI.as_view()),
    path('api/auth/register', UserRegistrationAPI.as_view()),
    path('api/auth/logout', knox_views.LogoutView.as_view()),
    path('api/auth/login', UserLoginAPI.as_view()),
    path('api/checkout_info/add/', PostCheckoutInfoAPI.as_view()),
    path('api/post_payment/<user_id>/', PostPaymentAPI.as_view()),
    path('api/payment/<user_id>/', PaymentAPI.as_view()),
    #_____API VIEWS END_____
    path('', HomeView.as_view(), name='home'),
    path('shop/', ShopView.as_view(), name="shop"),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('payment/', PaymentView.as_view(), name='payment'),
    path('payment_succeeded/', payment_succeeded, name='payment_succeeded'),
    path('contact/', ContactView.as_view(), name="contact"),
    path('secret/', secret, name='secret'),
    path('connect/get_oauth_url/', get_oauth_url, name='get_oauth_url'),
    path('connect/oauth/', handle_oauth_redirect, name='handle_oauth_redirect'),
    path('permission_denied/', permission_denied, name='permission_denied'),
    path('get_countries/', get_countries, name='get_countries'),
    path('get_regions/', get_regions, name='get_regions'),
    path('get_cities/', get_cities, name='get_cities'),
]


