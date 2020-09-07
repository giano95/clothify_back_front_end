from django.test import TestCase
from core.models import User, CheckoutInfo
from django.test.client import Client
from django.urls import reverse, resolve
from django.contrib.auth.models import Group
from core.forms import ContactForm

# Create your tests here

# Test case for the login of an User
class LogInTest(TestCase):

    def setUp(self):
        self.group = Group(name='Buyer')
        self.group.save()
    
        self.user = User.objects.create_user(
            first_name='abdul',
            last_name='lalla',
            username='esplodo95',
            email='allah.akbar@gmail.com',
            password='asdasd',
            user_type='Buyer'
        )

    def tearDown(self):
        self.group.delete()
        self.user.delete()

    def test_login(self):
        client = Client()
        response = client.post(reverse('account_login'), data={
            'username': 'esplodo95',
            'password': 'asdasd',
        })
        self.assertTrue(response.status_code == 200, 'Registrazione fallita')
        print("Login avvenuto con successo\n")

# Test case for the registration of an User
class RegistrationTest(TestCase):

    def setUp(self):
        self.group1 = Group(name='Buyer')
        self.group1.save()
        self.group2 = Group(name='SubSeller')
        self.group2.save()
        self.group3 = Group(name='UnsubSeller')
        self.group3.save()

    def tearDown(self):
        self.group1.delete()
        self.group2.delete()
        self.group3.delete()

    def test_buyer_registration(self):
        print("\nVerifica registrazione utente di tipo Buyer...")
        client = Client()
        response = client.post(reverse('account_signup'), data={
            'first_name': 'enri',
            'last_name': 'petrucci',
            'username': 'petrux95',
            'email': 'enri.petrucci@gmail.com',
            'password': 'asdasd',
            'password2': 'asdasd',
            'user_type': 'Buyer'
        })
        self.assertTrue(response.status_code == 200, 'Registrazione fallita')
        print("Registrazione avvenuta con successo\n")
    
    def test_seller_registration(self):
        print("\nVerifica registrazione utente di tipo Buyer...")
        client = Client()
        response = client.post(reverse('account_signup'), data={
            'first_name': 'enri',
            'last_name': 'petrucci',
            'username': 'petrux95',
            'email': 'enri.petrucci@gmail.com',
            'password': 'asdasd',
            'password2': 'asdasd',
            'user_type': 'Seller'
        })
        self.assertTrue(response.status_code == 200, 'Registrazione fallita')
        print("Registrazione avvenuta con successo\n")
    
    

class CheckoutInfoTest(TestCase):

    def setUp(self):
        self.group = Group(name='Buyer')
        self.group.save()
    
        self.user = User.objects.create_user(
            first_name='abdul',
            last_name='lalla',
            username='esplodo95',
            email='allah.akbar@gmail.com',
            password='asdasd',
            user_type='Buyer'
        )

    def tearDown(self):
        self.group.delete()
        self.user.delete()

    def test_checkoutinfo_creation(self):
        print("\nVerifica creazione CheckoutInfo...")
        checkout_info = CheckoutInfo.objects.create(
            user=self.user,
            first_name='enri',
            last_name='petrucci',
            email='enri.petrucci@gmail.com',
            first_address='via brombeis',
            country='Italy',
            region='Emilia-Romagna',
            city='Modena',
            zip_code='41026'
        )
        print(checkout_info)
        print("CheckoutInfo object creato con successo\n")

class ContactTest(TestCase):

    def test_forms(self):
        print("\nVerifica contact form...")
        contact_form = {'form_email': 'ciao@ciao.com', 'subject' : 'soggetto_test', 'message' : 'test'}
        form = ContactForm(data=contact_form)
        self.assertTrue(form.is_valid())
        print("Contact form giusto\n")
