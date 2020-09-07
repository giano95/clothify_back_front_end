from django.test import TestCase
from django.test.client import Client
from django.urls import reverse
from django.contrib.auth.models import Group
from item.models import *
from django.core.files import File
from django.contrib.auth import get_user_model
User = get_user_model()


class ItemCreateTest(TestCase):

    def setUp(self):

        self.group = Group(name='UnsubSeller')
        self.group.save()

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

        self.item = Item.objects.create(
            owner= self.user,
            name='test',
            price=10,
            category= self.item_category,
            description= 'test description',
            img='item/img/vintage_1_3.webp'
        )
        self.item.images.set([])
        self.item.color.set([self.item_color_1, self.item_color_2])
        self.item.quantities_size.set([self.item_quantity_size_1, self.item_quantity_size_2])

    def tearDown(self):
        self.group.delete()
        self.user.delete()
        self.item.delete()

    def test_item_create(self):
        print("\nVerifica creazione item...")

        # Create a client that we use for testing porpouse
        client = Client()

        # Login with that client
        response = client.login(username='esplodo95', password='asdasd')
        self.assertTrue(response, 'Login fallito: credenziali non corrette\n')

        # GET the resposnse from ItemView and verify the correct creation of the item
        response = client.get(reverse('item:item', kwargs={'pk': self.item.id}))
        item = response.context['item']
        print(item.name)
        print("Creazione item avvenuta con successo\n")

class ItemDeleteTest(TestCase):

    def setUp(self):

        self.group = Group(name='UnsubSeller')
        self.group.save()

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

        self.item = Item.objects.create(
            owner= self.user,
            name='test',
            price=10,
            category= self.item_category,
            description= 'test description',
            img='item/img/vintage_1_3.webp'
        )
        self.item.images.set([])
        self.item.color.set([self.item_color_1, self.item_color_2])
        self.item.quantities_size.set([self.item_quantity_size_1, self.item_quantity_size_2])

    def tearDown(self):
        self.group.delete()
        self.user.delete()
        self.item.delete()

    def test_item_create(self):
        print("\nVerifica eliminazione item...")

        # Create a client that we use for testing porpouse
        client = Client()

        # Login with that client
        response = client.login(username='esplodo95', password='asdasd')
        self.assertTrue(response, 'Login fallito: credenziali non corrette\n')

        # GET the resposnse from DeleteItemView and verify the correct deleting of the item
        response = client.get(reverse('item:delete', kwargs={'pk': self.item.id}))
        print(Item.objects.all())
        print("eliminazione item avvenuta con successo\n")

class ItemReviewPostTest(TestCase):

    def setUp(self):

        self.group = Group(name='UnsubSeller')
        self.group.save()

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

        self.item = Item.objects.create(
            owner= self.user,
            name='test',
            price=10,
            category= self.item_category,
            description= 'test description',
            img='item/img/vintage_1_3.webp'
        )
        self.item.images.set([])
        self.item.color.set([self.item_color_1, self.item_color_2])
        self.item.quantities_size.set([self.item_quantity_size_1, self.item_quantity_size_2])

    def tearDown(self):
        self.group.delete()
        self.user.delete()
        self.item.delete()

    def test_item_create(self):
        print("\nVerifica post ItemReview...")

        # Create a client that we use for testing porpouse
        client = Client()

        # Login with that client
        response = client.login(username='esplodo95', password='asdasd')
        self.assertTrue(response, 'Login fallito: credenziali non corrette\n')

        # GET the resposnse from ItemView and verify the correct creation of the item
        response = client.post(reverse('item:item', kwargs={'pk': self.item.id}), data={
            'title': 'review di prova',
            'comment': 'questo è un commento di prova ma spacca lo stesso',
            'vote': 4
        })
        item_reviews = ItemReview.objects.filter(user=self.user, item=self.item).all()
        print(item_reviews)
        print("Post ItemReview avvenuta con successo\n")

class PostItemTest(TestCase):

    def setUp(self):

        self.group1 = Group(name='Buyer')
        self.group1.save()
        self.group2 = Group(name='SubSeller')
        self.group2.save()
        self.group3 = Group(name='UnsubSeller')
        self.group3.save()

        self.user = User.objects.create_user(
            first_name='test',
            last_name='test',
            username='test95',
            email='test.test@gmail.com',
            password='test',
            user_type='Seller'
        )

        self.user.groups.add(self.group2)
        self.user.groups.remove(self.group3)

        self.item_category = ItemCategory.objects.create(name='Jeans')
        self.item_color_1 = ItemColor.objects.create(name='blu')
        self.item_color_2 = ItemColor.objects.create(name='giallo')

    def test_form_item(self):
        print("\nVerifica inserimento item...")

        client = Client()

        response = client.login(username='test95', password='test')
        self.assertTrue(response, 'Login fallito: credenziali non corrette\n')

        img = open('media/item/img/vintage_1_3.webp', 'rb')
        img_file = File(img)

        response = client.post(reverse('item:add'), data={
            'name': 'test',
            'description': 'test description',
            'price': 1000.0,
            'color': [self.item_color_1.id, self.item_color_2.id],
            'category' : self.item_category.id,
            'img' : img_file,
            'form-TOTAL_FORMS': ['3', '6'],
            'form-INITIAL_FORMS': ['0', '0'],
            'form-MIN_NUM_FORMS': ['0', '0'],
            'form-MAX_NUM_FORMS': ['1000', '1000'],
        })

        item = Item.objects.filter(price=1000)
        self.assertTrue(len(item) == 1, 'Inserimento item fallito..')

        print("Inserimento item avvenuto con successo\n")
        