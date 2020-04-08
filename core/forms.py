from django import forms
from django_countries.fields import CountryField


PAYMENT_CHOICES = (
    ('S', 'Stripe'),
    ('P', 'PayPal')
)


class CheckoutForm(forms.Form):
    firstName = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'First name'
    }))
    lastName = forms.CharField()
    eMail = forms.EmailField(required=False)
    address = forms.CharField()
    address2 = forms.CharField(required=False)
    country = CountryField(blank_label='(select country)')
    zip_ = forms.CharField()
    sameBillingAddress = forms.BooleanField(widget=forms.CheckboxInput())
    saveInfo = forms.BooleanField(widget=forms.CheckboxInput())
    paymentOption = forms.ChoiceField(
        widget=forms.RadioSelect(), choices=PAYMENT_CHOICES)
