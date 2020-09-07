from django import forms
from django.conf import settings
from django.forms import TextInput, Select, PasswordInput, FileInput, CheckboxInput, RadioSelect
from cities_light.models import Country, Region, City
from django.contrib.auth.forms import UserCreationForm
from core.models import User
from django.contrib.auth.forms import UserCreationForm
from allauth.account.forms import LoginForm
import json as json
from core.models import CheckoutInfo


class CustomUserCreationForm(UserCreationForm):
    user_type = forms.ChoiceField(choices=User.TYPE_CHOICES, label='User Type')
    profile_img = forms.ImageField(
        widget=FileInput(attrs={'id': 'id_profile_img'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username',
                  'user_type', 'email', 'password1', 'password2', 'profile_img')
        widgets = {
            'first_name': TextInput(attrs={'id': 'first_name', 'class': 'form-control'}),
            'last_name': TextInput(attrs={'id': 'last_name', 'class': 'form-control'}),
            'username': TextInput(attrs={'id': 'username', 'class': 'form-control'}),
            'email': TextInput(attrs={'id': 'email', 'class': 'form-control'}),
            'password1': PasswordInput(attrs={'id': 'password1', 'class': 'form-control password-form'}),
            'password2': PasswordInput(attrs={'id': 'password2', 'class': 'form-control password-form'}),
        }

        def signup(self, request, user):
            pass


class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)

        self.fields['password'].widget = PasswordInput(
            attrs={'id': 'password', 'class': 'form-control password-form mb-0'})
        self.fields['login'].widget = TextInput(
            attrs={'id': 'login', 'class': 'form-control mb-0'})


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
   


class ContactForm(forms.Form):

    form_email = forms.EmailField(widget=forms.EmailInput(
        attrs={'id': 'form_email', 'class': 'form-control', 'type': 'email'}), required=True)
    subject = forms.CharField(widget=forms.TextInput(
        attrs={'id': 'subject', 'class': 'form-control', 'type': 'text'}), required=True)
    message = forms.CharField(widget=forms.Textarea(
        attrs={'id': 'message', 'class': 'md-textarea form-control', 'rows': '4'}), required=True)
