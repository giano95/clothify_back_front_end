from django.test import TestCase
from django.test.client import Client
from django.urls import reverse
from django.contrib.auth.models import Group
from order.models import OrderItem, Order
from item.models import *
from django.contrib.auth import get_user_model
User = get_user_model()


class OrderTest(TestCase):

    def setUp(self):

        self.group1 = Group(name='Buyer')
        self.group1.save()
        self.group2 = Group(name='SubSeller')
        self.group2.save()
        self.group3 = Group(name='UnsubSeller')
        self.group3.save()

        self.user = User.objects.create_user(
            first_name='abdul',
            last_name='lalla',
            username='esplodo95',
            email='allah.akbar@gmail.com',
            password='asdasd',
            user_type='Seller'
        )

        self.item_category = ItemCategory.objects.create(name='Jeans')
        self.item_color_1 = ItemColor.objects.create(name='blu')
        self.item_color_2 = ItemColor.objects.create(name='giallo')
        self.item_size_1 = ItemSize.objects.create(tag='S')
        self.item_size_2 = ItemSize.objects.create(tag='M')
        self.item_quantity_size_1 = ItemQuantitySize.objects.create(size=self.item_size_1, quantity=10)
        self.item_quantity_size_2 = ItemQuantitySize.objects.create(size=self.item_size_2, quantity=5)

        self.item_1 = Item.objects.create(
            owner= self.user,
            name='test',
            price=10,
            category= self.item_category,
            description= 'test description',
            img='item/img/vintage_1_3.webp'
        )
        self.item_1.images.set([])
        self.item_1.color.set([self.item_color_1, self.item_color_2])
        self.item_1.quantities_size.set([self.item_quantity_size_1, self.item_quantity_size_2])

        self.order_item_1 = OrderItem.objects.create(
            user= self.user,
            item=self.item_1,
            item_size=self.item_size_1,
            is_ordered=False,
            pending=False,
            quantity=1
        )
        self.order_item_2 = OrderItem.objects.create(
            user= self.user,
            item=self.item_1,
            item_size=self.item_size_2,
            is_ordered=False,
            pending=False,
            quantity=3
        )
        

        self.order = Order.objects.create(
            user=self.user,
            is_ordered=False
        )
        self.order.order_items.set([self.order_item_1, self.order_item_2])

    def tearDown(self):
        self.group1.delete()
        self.group2.delete()
        self.group3.delete()
        self.user.delete()
        self.order_item_1.delete()
        self.order.delete()


    def test_order(self):
        print("\nVerifica creazione order...")
        client = Client()
        response = client.login(username='esplodo95', password='asdasd')
        self.assertTrue(response, 'Login fallito: credenziali non corrette\n')
        response = client.get(reverse('order:order'))
        order = response.context['order']
        order_items = order.order_items.all()
        print(order_items)
        print("Creazione order avvenuta con successo\n")
