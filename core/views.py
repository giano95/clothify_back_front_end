from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, View
from django.utils import timezone
from django.contrib import messages
from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from .models import Item, OrderItem, Order
from cities_light.models import Country, Region
from .forms import CheckoutForm


class HomeView(ListView):
    model = Item
    paginate_by = 4
    template_name = 'home.html'


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
        form = CheckoutForm()
        return render(self.request, "checkout.html", {'form': form})

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        if form.is_valid():
            return redirect('core:checkout')


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
