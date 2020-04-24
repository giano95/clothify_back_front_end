from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views.generic import ListView, DetailView, View
from django.utils import timezone
from django.contrib import messages
from django.http import Http404, JsonResponse, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from password_generator import PasswordGenerator
from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.contrib.auth.decorators import permission_required
from django.template.loader import render_to_string
import operator
from functools import reduce

from .models import CheckoutInfo, Item, OrderItem, Order, User
from .forms import CheckoutForm, ItemForm
from cities_light.models import Country, Region, City

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
suggested_capabilities = 'transfers'
stripe_user = {'email': 'user@example.com'}


@login_required
@permission_required('core.add_item', raise_exception=True)
def get_oauth_url(request):
    oauth_url = 'https://connect.stripe.com/express/oauth/authorize?' + \
        'client_id=' + 'ca_H86KCmvSbEJXwyLilNw2t3wV9a1jNDZW' + \
        '&state=' + state + \
        '&suggested_capabilities[]=' + 'transfers' + \
        '&stripe_user[email]=' + request.user.email + \
        '&stripe_user[first_name]=' + request.user.first_name + \
        '&stripe_user[last_name]=' + request.user.last_name
    return JsonResponse({'oauth_url': oauth_url})


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

    connected_account_id = response['stripe_user_id']
    request.user.connected_account_id = connected_account_id
    request.user.save()

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


""" class HomeView(ListView):
    model = Item
    paginate_by = 4
    template_name = 'home.html'

    def get_queryset(self):
        result = super(HomeView, self).get_queryset()

        query = self.request.GET.get('q')
        if query:
            query = Item.objects.filter(name__icontains=query)
            result = query
        return result """


def items_view(request):

    ctx = {}
    url_parameter = request.GET.get("q")

    if url_parameter:
        items = Item.objects.filter(name__icontains=url_parameter)
    else:
        items = Item.objects.all()

    ctx["items"] = items

    if request.is_ajax():
        html = render_to_string(
            template_name="items-results-partial.html",
            context={"items": items}
        )

        data_dict = {"html_from_view": html}

        return JsonResponse(data=data_dict, safe=False)

    return render(request, 'home.html', context=ctx)


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        order = Order.objects.filter(user=self.request.user, is_ordered=False)
        if not order.exists():
            messages.error(request, 'You doesn\'t have any active order')
            return redirect('core:home')
        else:
            return render(self.request, 'order-summary.html', {'order': order[0]})


class ItemView(DetailView):
    model = Item
    template_name = 'item.html'


class CheckoutView(View):

    def get(self, *args, **kwargs):
        print(self.request.user.connected_account_id)
        form = CheckoutForm()
        return render(self.request, "checkout.html", {'form': form})

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        order = Order.objects.filter(
            user=self.request.user,
            is_ordered=False
        )
        if not order.exists() or not form.is_valid():
            messages.warning(self.request, "Failed checkout")
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


@login_required
@permission_required('core.add_item', raise_exception=True)
def add_post(request):
    form = ItemForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        item = form.save()
        item.refresh_from_db()
        item.owner = request.user
        item.name = form.cleaned_data.get('name')
        item.description = form.cleaned_data.get('description')
        item.category = form.cleaned_data.get('category')
        item.price = form.cleaned_data.get('price')
        item.unit = form.cleaned_data.get('unit')
        item.img = form.cleaned_data.get('img')
        item.save()
        messages.success(request, 'Post created!', extra_tags='fa fa-check')
        return redirect(item.get_url())
    else:
        return render(request, 'post_form.html', {'form': form})
    return render(request, 'post_form.html', {'form': form})


@login_required
def add_to_cart(request, pk):
    item = Item.objects.filter(pk=pk)
    if not item.exists():
        messages.info(request, 'this item doesn\'t exists')
        return redirect('core:item', pk=pk)
    item = item[0]
    order_item, _ = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        is_ordered=False
    )
    order = Order.objects.filter(
        user=request.user,
        is_ordered=False
    )
    if not order.exists():
        order = Order.objects.create(
            user=request.user,
            ordered_date=timezone.now()
        )
        order.order_items.add(order_item)
    else:
        order = order[0]
        if order.order_items.filter(item__pk=pk).exists():
            order_item.quantity += 1
            order_item.save()
        else:
            order.order_items.add(order_item)
    messages.success(request, 'item added on the cart successfully')
    return redirect('core:item', pk=pk)


@login_required
def update_cart(request, pk, q):
    item = Item.objects.filter(pk=pk)
    if not item.exists():
        messages.warning(request, 'update_cart: item doesn\'t exists')
        return redirect('core:order_summary')
    item = item[0]

    order_item = OrderItem.objects.filter(
        item=item,
        user=request.user,
        is_ordered=False
    )
    if not order_item.exists():
        messages.warning(request, 'update_cart: order_item doesn\'t exists')
        return redirect('core:order_summary')
    order_item = order_item[0]

    order = Order.objects.filter(
        user=request.user,
        is_ordered=False
    )
    if not order.exists():
        messages.warning(request, 'update_cart: order doesn\'t exists')
        return redirect('core:order_summary')
    order = order[0]

    if not order.order_items.filter(item__pk=pk).exists():
        messages.warning(
            request, 'update_cart: order_item isn\'t in your cart')
        return redirect('core:order_summary')

    if q == '0':
        order_item.delete()
    else:
        order_item.quantity = q
        order_item.save()

    return redirect('core:order_summary')


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
    if group_name != 'Buyer' and group_name != 'Seller':
        return
    group = Group.objects.get(name=group_name)
    group.user_set.add(instance)


post_save.connect(set_group, sender=User)


def tmp(request):
    return render(request, "tmp/home.html", context={})
