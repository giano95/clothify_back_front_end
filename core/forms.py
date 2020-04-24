from django import forms
from django.conf import settings
from django.forms import TextInput, Select
from cities_light.models import Country, Region, City
from django.contrib.auth.forms import UserCreationForm
from .models import User, CheckoutInfo, Item
from django.contrib.auth.forms import UserCreationForm
import json as json

PAYMENT_CHOICES = (
    ('sripe', 'stripe'),
    ('paypal', 'paypal')
)


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = CheckoutInfo
        exclude = ['user']
        widgets = {
            'first_name': TextInput(attrs={'id': 'first_name', 'class': 'form-control'}),
            'last_name': TextInput(attrs={'id': 'last_name', 'class': 'form-control'}),
            'email': TextInput(attrs={'id': 'email', 'class': 'form-control py-0', 'placeholder': 'local-part@domain'}),
            'first_address': TextInput(attrs={'id': 'first_address', 'class': 'form-control'}),
            'billing_address': TextInput(attrs={'id': 'billing_address', 'class': 'form-control'}),
            'country': Select(attrs={'class': 'custom-select d-block w-100'}),
            'region': Select(attrs={'class': 'custom-select d-block w-100'}),
            'city': Select(attrs={'class': 'custom-select d-block w-100'}),
            'zip_code': TextInput(attrs={'id': 'zip_code', 'class': 'form-control'}),
        }
    PAYMENT_CHOICES = (
        ('S', 'Stripe'),
        ('P', 'PayPal')
    )

    same_billing_address = forms.BooleanField(widget=forms.CheckboxInput(attrs={
        'id': 'same_billing_address',
        'class': 'custom-control-input'
    }))
    save_info = forms.BooleanField(widget=forms.CheckboxInput(attrs={
        'id': 'save_info',
        'class': 'custom-control-input'
    }))
    payment_option = forms.ChoiceField(
        choices=PAYMENT_CHOICES, widget=forms.RadioSelect)


class CustomUserCreationForm(UserCreationForm):
    user_type = forms.ChoiceField(choices=User.TYPE_CHOICES, label='User Type')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username',
                  'email', 'user_type', 'password1', 'password2')

        def signup(self, request, user):
            pass


class ItemForm(forms.ModelForm):
    img = forms.ImageField(help_text="Upload image: ", required=True)
    name = forms.CharField(max_length=100, help_text='title')
    category = forms.ChoiceField(
        choices=Item._meta.get_field('category').choices)
    description = forms.CharField(max_length=1000)
    price = forms.DecimalField(max_digits=7, decimal_places=2)
    unit = forms.ChoiceField(choices=Item._meta.get_field('unit').choices)

    class Meta:
        model = Item
        fields = ['name', 'description', 'category', 'price', 'img', 'unit']
