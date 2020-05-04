from django.shortcuts import render, redirect
from django.views.generic import View
from order.models import Order, OrderItem
from item.models import Item, ItemSize
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.utils.decorators import method_decorator


@method_decorator(login_required, name='dispatch')
class OrderView(View):
    def get(self, *args, **kwargs):
        order = Order.objects.filter(
            user=self.request.user, is_ordered=False)
        if not order.exists():
            return render(self.request, 'order-summary2.html', {'order': None})
        else:
            return render(self.request, 'order-summary2.html', {'order': order[0]})


@method_decorator(login_required, name='dispatch')
class AddOrderItemView(View):
    def get(self, *args, **kwargs):

        item = Item.objects.filter(pk=kwargs['pk'])
        if not item.exists():
            print('this item doesn\'t exists')
            return redirect('item:item', pk=kwargs['pk'])
        item = item[0]

        order_item, _ = OrderItem.objects.get_or_create(
            item=item,
            user=self.request.user,
            is_ordered=False,
            item_size=ItemSize.objects.get(tag=kwargs['sz'])
        )
        order = Order.objects.filter(
            user=self.request.user,
            is_ordered=False
        )
        if not order.exists():
            order = Order.objects.create(
                user=self.request.user,
                ordered_date=timezone.now()
            )
            order_item.quantity = int(kwargs['q'])
            order_item.save()
            order.order_items.add(order_item)
        else:
            order = order[0]
            if order.order_items.filter(item__pk=kwargs['pk']).exists():
                order_item.quantity += int(kwargs['q'])
                order_item.save()
            else:
                order_item.quantity = int(kwargs['q'])
                order_item.save()
                print(kwargs['q'])
                order.order_items.add(order_item)
        print('item added on the order successfully')
        return redirect('item:item', pk=kwargs['pk'])

    def post(self, *args, **kwargs):
        pass


@method_decorator(login_required, name='dispatch')
class UpdateOrderItemView(View):
    def get(self, *args, **kwargs):
        item = Item.objects.filter(pk=kwargs['pk'])
        if not item.exists():
            print('update_cart: item doesn\'t exists')
            return redirect('order:order')
        item = item[0]

        order_item = OrderItem.objects.filter(
            item=item,
            user=self.request.user,
            is_ordered=False
        )
        if not order_item.exists():
            print('update_cart: order_item doesn\'t exists')
            return redirect('order:order')
        order_item = order_item[0]

        order = Order.objects.filter(
            user=self.request.user,
            is_ordered=False
        )
        if not order.exists():
            print('update_cart: order doesn\'t exists')
            return redirect('order:order')
        order = order[0]

        if not order.order_items.filter(item__pk=kwargs['pk']).exists():
            print('update_cart: order_item isn\'t in your cart')
            return redirect('order:order')

        if kwargs['q'] == '0':
            order_item.delete()
        else:
            order_item.quantity = kwargs['q']
            order_item.save()

        return redirect('order:order')

    def post(self, *args, **kwargs):
        pass
