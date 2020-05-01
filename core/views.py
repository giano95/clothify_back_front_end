from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views.generic import ListView, DetailView, View
from django.utils import timezone
from django.contrib import messages
from django.http import Http404, JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import auth
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from password_generator import PasswordGenerator
from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.template.loader import render_to_string
from django.db.models import Count
from django.core.mail import send_mail, BadHeaderError
from django.forms import modelformset_factory
from django.template import RequestContext

from core.models import User
from core.forms import ContactForm, CheckoutForm
from cities_light.models import Country, Region, City
from item.models import Item, ItemCategory, ItemColor, ItemImage, ItemLabel, ItemReview, ItemSize


import stripe
import json


# Set your secret key. Remember to switch to your live secret key in production!
# See your keys here: https://dashboard.stripe.com/account/apikeys
stripe.api_key = 'sk_test_Serg3AwZr2ANOTEhDS7rGbEb00MsOgU1oX'

# Unique, not guessable value used to prevent CSRF attacks
pwo = PasswordGenerator()
state = pwo.shuffle_password(
    'QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm1234567890-_', 12)

# temporary fields
client_id = 'ca_H86KCmvSbEJXwyLilNw2t3wV9a1jNDZW'


def is_unsub_seller(user):
    if user.groups.filter(name='UnsubSeller').exists() and user.get_user_type() == 'Seller':
        return True
    else:
        return False


def is_sub_seller(user):
    if user.groups.filter(name='SubSeller').exists() and user.get_user_type() == 'Seller':
        return True
    else:
        return False


class ShopView(ListView):
    model = Item
    paginate_by = 9
    context_object_name = 'items'
    template_name = 'shop.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ShopView, self).get_context_data(*args, **kwargs)

        # set in the context the categories objects
        context['categories'] = ItemCategory.objects.all()
        context['colors'] = [color[0] for color in ItemColor.CHOICES]
        context['sizes'] = [size[0] for size in ItemSize.CHOICES]

        # if there are some url parameters also save them in the context
        context['category_name'] = (
            self.request.GET.get('category_name') or None)
        context['query_text'] = (self.request.GET.get('query_text') or None)
        reviews_vote = (self.request.GET.get('reviews_vote') or None)
        if reviews_vote:
            context['reviews_vote'] = int(reviews_vote)
        from_price = (self.request.GET.get('from_price') or None)
        if from_price:
            context['from_price'] = int(from_price)
        to_price = (self.request.GET.get('to_price') or None)
        if to_price:
            context['to_price'] = int(to_price)
        colors_name = (self.request.GET.get('colors_name') or None)
        if colors_name:
            context['colors_name'] = colors_name.split(",")[:-1]
        sizes_tag = (self.request.GET.get('sizes_tag') or None)
        if sizes_tag:
            context['sizes_tag'] = sizes_tag.split(",")[:-1]

        return context

    def get_queryset(self):
        result = super(ShopView, self).get_queryset()

        # Filter by the category
        category_name = self.request.GET.get('category_name')
        if category_name:
            items = Item.objects.filter(category__name=category_name)
            result = items

        # Filter by the some query text
        query_text = self.request.GET.get('query_text')
        if query_text:
            items = Item.objects.filter(name__icontains=query_text)
            result = items

        # Filter by the avg reviews vote
        reviews_vote = self.request.GET.get('reviews_vote')
        if reviews_vote:
            items = []
            for item in Item.objects.all():
                if int(reviews_vote) == item.reviews_vote:
                    items.append(item)
            result = items

        # Filter by the price
        from_price = self.request.GET.get('from_price')
        to_price = self.request.GET.get('to_price')
        if from_price and to_price:
            items = Item.objects.filter(
                price__range=(int(from_price), int(to_price)))
            result = items
        elif from_price:
            items = Item.objects.filter(price__gte=int(from_price))
            result = items
        elif to_price:
            items = Item.objects.filter(price__lte=int(to_price))
            result = items

        # Filter by the colors
        colors_name = (self.request.GET.get('colors_name') or None)
        if colors_name:
            colors_name = colors_name.split(",")[:-1]
            for size in Item.objects.all().values_list('color'):
                print(size)
            items = Item.objects.all().filter(color__name__in=colors_name).distinct()
            result = items

        # Filter by the size
        sizes_tag = (self.request.GET.get('sizes_tag') or None)
        if sizes_tag:
            sizes_tag = sizes_tag.split(",")[:-1]

            items = Item.objects.all().filter(size__tag__in=sizes_tag).distinct()
            result = items

        return result


class HomeView(ListView):
    model = Item
    paginate_by = 6
    context_object_name = 'items'
    template_name = 'home.html'

    def get_context_data(self, *args, **kwargs):
        context = super(HomeView, self).get_context_data(*args, **kwargs)
        context['categories'] = ItemCategory.objects.all()
        return context


class CheckoutView(View):

    def get(self, *args, **kwargs):
        form = CheckoutForm()
        return render(self.request, "checkout.html", {'form': form})

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        order = Order.objects.filter(
            user=self.request.user,
            is_ordered=False
        )
        if not order.exists() or not form.is_valid():
            print("Failed checkout")
            return render(self.request, 'checkout.html', {'form': form})

        order = order[0]
        checkout_info = form.save(commit=False)
        checkout_info.user = self.request.user
        checkout_info.save()
        form.save_m2m()
        order.checkout_info = checkout_info
        order.save()
        return redirect('core:payment', payment_option=form.cleaned_data['payment_option'])


class PaymentView(View):

    def get(self, *args, **kwargs):
        return render(self.request, "payment.html", context={})


class ContactView(View):
    def get(self, *args, **kwargs):
        form = ContactForm()
        return render(self.request, 'contact.html', {'form': form})

    def post(self, *args, **kwargs):
        form = ContactForm(self.request.POST or None)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['form_email']
            message = form.cleaned_data['message']
            try:
                send_mail(subject, message, from_email, [
                          'marco.gianelli.95@gmail.com'])
                messages.success(
                    self.request, 'Success! Thank you for your message.')
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('core:contact')
        else:
            messages.warning(self.request, form.errors.as_data())
        return render(self.request, 'contact.html', {'form': form})


@login_required
@user_passes_test(is_unsub_seller)
def get_oauth_url(request):
    oauth_url = 'https://connect.stripe.com/express/oauth/authorize?' + \
        'client_id=' + 'ca_H86KCmvSbEJXwyLilNw2t3wV9a1jNDZW' + \
        '&state=' + state + \
        '&suggested_capabilities[]=' + 'transfers' + \
        '&stripe_user[email]=' + request.user.email + \
        '&stripe_user[first_name]=' + request.user.first_name + \
        '&stripe_user[last_name]=' + request.user.last_name
    return JsonResponse({'oauth_url': oauth_url})


# A dummy url fo redirect the non seller who try to get the oauth url
def dummy_url(request):
    return JsonResponse({'error': '403 Forbidden: you are not a Seller'}, status=403)


def handle_oauth_redirect(request):
    # Assert the state matches the state you provided in the OAuth link (optional)
    this_state = request.GET.get('state')
    if this_state != state:
        return JsonResponse({'error': 'Incorrect state parameter: ' + this_state}, status=403)

    # Send the authorization code to Stripe's API.
    code = request.GET.get('code')
    try:
        response = stripe.OAuth.token(
            grant_type='authorization_code', code=code,)
    except stripe.oauth_error.OAuthError as e:
        return JsonResponse({'error': 'Invalid authorization code: ' + code}, status=400)
    except Exception as e:
        return JsonResponse({'error': 'An unknown error occurred.'}, status=500)

    # Get the connected_account_id and save it
    connected_account_id = response['stripe_user_id']
    request.user.connected_account_id = connected_account_id
    request.user.save()

    # Promote the user to a SubSeller
    group = Group.objects.get(name='SubSeller')
    request.user.groups.add(group)
    group = Group.objects.get(name='UnsubSeller')
    request.user.groups.remove(group)

    # Render some HTML or redirect to a different page.
    messages.success(request, 'redirection handled successfully')
    return redirect('core:home')


@login_required
def secret(request):

    order = Order.objects.filter(
        user=request.user,
        is_ordered=False
    )
    order_items = OrderItem.objects.filter(
        user=request.user,
        is_ordered=False
    )
    if not order.exists() or not order_items.exists():
        print('order_error or order_items_error')
        return JsonResponse({'client_secret': 'error'})

    order = order[0]
    order_items = order_items[0]
    connected_account_id = order_items.item.owner.connected_account_id

    if connected_account_id is None:
        print('connected_account_id_error')
        return JsonResponse({'client_secret': 'error'})

    amount = round(order.get_total_order_price() * 100.0)
    application_fee_amount = round(0.123 * amount)
    print(amount)
    print(application_fee_amount)

    intent = stripe.PaymentIntent.create(
        payment_method_types=['card'],
        amount=amount,
        currency='eur',
        application_fee_amount=application_fee_amount,
        transfer_data={
            'destination': connected_account_id,
        }
    )
    return JsonResponse({'client_secret': intent.client_secret})


def get_countries(request):
    countries = list(Country.objects.values_list(
        'name', flat=True).order_by('name'))
    return JsonResponse({'countries': countries})


def get_regions(request):
    country_name = request.GET.get('country_name')
    country = Country.objects.get(name=country_name)
    regions = list(Region.objects.filter(country_id=country.id).values_list(
        'name', flat=True).order_by('name'))
    return JsonResponse({'regions': regions})


def get_cities(request):
    region_name = request.GET.get('region_name')
    region = Region.objects.get(name=region_name)
    cities = list(City.objects.filter(region_id=region.id).values_list(
        'name', flat=True).order_by('name'))
    return JsonResponse({'cities': cities})


def set_group(sender, instance, **kwargs):
    group_name = instance.get_user_type()

    # if the user already belogn to a group pass
    if instance.groups.filter(name__in=['Buyer', 'UnsubSeller', 'SubSeller']).exists():
        return
    elif group_name == 'Buyer':
        group = Group.objects.get(name='Buyer')
        group.user_set.add(instance)
    elif group_name == 'Seller':
        group = Group.objects.get(name='UnsubSeller')
        group.user_set.add(instance)


post_save.connect(set_group, sender=User)
