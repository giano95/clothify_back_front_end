from django import forms
from cities_light.models import Country, Region, City
import json as json

PAYMENT_CHOICES = (
    ('S', 'Stripe'),
    ('P', 'PayPal')
)


def init():

    dict_countries = []
    list_countries = []
    for country in Country.objects.all():
        dict_countries.append(str(country))
        list_countries.append((str(country), str(country)))

    dict_regions = {}
    list_regions = []
    for region in Region.objects.all():
        if region.country:
            if region.country.name in dict_regions:
                dict_regions[region.country.name].append(region.name)
            else:
                dict_regions[region.country.name] = [region.name]
            list_regions.append((region.name, region.name))

    dict_cities = {}
    list_cities = []
    for city in City.objects.all():
        if city.region:
            if city.region.name in dict_cities:
                dict_cities[city.region.name].append(city.name)
            else:
                dict_cities[city.region.name] = [city.name]
            list_cities.append((city.name, city.name))

    return (dict_countries, list_countries, dict_regions, list_regions, dict_cities, list_cities)


class CheckoutForm(forms.Form):
    dict_countries, list_countries, dict_regions, list_regions, dict_cities, list_cities = init()

    firstName = forms.CharField(widget=forms.TextInput(attrs={
        'id': 'firstName',
        'class': 'form-control'
    }))
    lastName = forms.CharField(widget=forms.TextInput(attrs={
        'id': 'lastName',
        'class': 'form-control'
    }))
    userName = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-0',
        'placeholder': 'Username'
    }))
    email = forms.EmailField(widget=forms.TextInput(attrs={
        'id': 'email',
        'class': 'form-control',
        'placeholder': 'youremail@example.com'
    }))
    address = forms.CharField(widget=forms.TextInput(attrs={
        'id': 'address',
        'class': 'form-control',
        'placeholder': '1234 Main St'
    }))
    address2 = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'id': 'address-2',
        'class': 'form-control',
        'placeholder': 'Apartment or suite'
    }))
    country = forms.ChoiceField(choices=(list_countries), widget=forms.Select(attrs={
        'class': 'custom-select d-block w-100'
    }))
    region = forms.ChoiceField(choices=(list_regions), widget=forms.Select(attrs={
        'class': 'custom-select d-block w-100'
    }))
    city = forms.ChoiceField(choices=(list_cities), widget=forms.Select(attrs={
        'class': 'custom-select d-block w-100'
    }))
    zip = forms.CharField()
    sameBillingAddress = forms.BooleanField(widget=forms.CheckboxInput())
    saveInfo = forms.BooleanField(widget=forms.CheckboxInput())
    paymentOption = forms.ChoiceField(
        widget=forms.RadioSelect(), choices=PAYMENT_CHOICES)

    countries = json.dumps(dict_countries)
    regions = json.dumps(dict_regions)
    cities = json.dumps(dict_cities)
