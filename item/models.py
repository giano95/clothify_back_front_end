from django.db import models
from django.conf import settings
from django.shortcuts import reverse
from django.contrib.auth.models import User
from statistics import mean
from math import ceil

LOREM_IPSUM = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris id turpis porttitor, vestibulum massa vel, tristique ante. Curabitur hendrerit quam massa, sit amet lobortis tellus consectetur eu. Suspendisse aliquet commodo tristique. Vivamus maximus pharetra sapien, ornare tempor libero egestas sed. Phasellus massa magna, tincidunt vitae nisl eget, rhoncus bibendum enim. Duis sed lectus sed leo pharetra ultrices id sit amet dolor. Vivamus pellentesque mi sed dignissim rhoncus. Nunc in sollicitudin quam. Nullam ornare dui quis sapien bibendum, nec sagittis purus venenatis.'
DEFAULT_IMG = 'https://mdbootstrap.com/img/Photos/Horizontal/E-commerce/Vertical/15.jpg'


class Item(models.Model):

    id = models.AutoField(primary_key=True)

    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.FloatField()
    category = models.ForeignKey('item.ItemCategory', on_delete=models.CASCADE)
    description = models.CharField(max_length=1000, default=LOREM_IPSUM)
    img = models.ImageField(upload_to='item/img/')
    color = models.ManyToManyField('item.ItemColor')
    size = models.ManyToManyField('item.ItemSize')
    quantity = models.IntegerField()
    label = models.ForeignKey(
        'item.ItemLabel', on_delete=models.CASCADE, null=True, blank=True)
    not_discounted_price = models.FloatField(blank=True, null=True)

    @property
    def reviews_vote(self):
        votes_qs = ItemReview.objects.filter(item=self).values_list('vote')
        if not votes_qs:
            return '0'

        votes = []
        for vote in votes_qs:
            votes.append(vote[0])

        avg = mean(votes)
        return ceil(avg)

    def get_price(self):
        return self.price

    def get_discount(self):
        if self.not_discounted_price:
            return self.not_discounted_price - self.price
        else:
            return 0

    def get_recommended_item(self):
        if self.category:
            return Item.objects.filter(category=self.category).exclude(id=self.id)[:4]
        else:
            return 0

    def get_url(self):
        return reverse('item:item', kwargs={'pk': self.id})

    def get_add_to_cart_url(self):
        return reverse('order:add_order_item', kwargs={'pk': self.id})

    def __str__(self):
        return self.name


def get_image_filename(instance, filename):
    id = instance.item.id
    return "post_images/%s" % (id)


class ItemImage(models.Model):
    item = models.ForeignKey('item.Item', on_delete=models.CASCADE, default='')
    image = models.ImageField(
        upload_to=get_image_filename, verbose_name='Image')

    def __str__(self):
        return 'ItemImage of {} item'.format(self.item.name)


class ItemReview(models.Model):
    VOTE_CHOICES = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    )
    comment = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    vote = models.IntegerField(choices=VOTE_CHOICES)
    img = models.ImageField(upload_to='item/category/img/',
                            blank=True, null=True)
    item = models.ForeignKey('item.Item', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.__str__() + '\'s review of the ' + self.item.__str__() + 'item!'


class ItemColor(models.Model):
    CHOICES = (
        ('white', 'white'),
        ('grey', 'grey'),
        ('black', 'black'),
        ('green', 'green'),
        ('blue', 'blue'),
        ('purple', 'purple'),
        ('yellow', 'yellow'),
        ('indigo', 'indigo'),
        ('red', 'red'),
        ('orange', 'orange')
    )

    name = models.CharField(choices=CHOICES, max_length=10)

    def __str__(self):
        return self.name


class ItemSize(models.Model):
    CHOICES = (
        ('XS', 'XS'),
        ('S', 'S'),
        ('M', 'M'),
        ('L', 'L'),
        ('XL', 'XL'),
        ('XXL', 'XXL')
    )

    tag = models.CharField(choices=CHOICES, max_length=3)

    def __str__(self):
        return self.tag


class ItemLabel(models.Model):
    CHOICES = (
        ('badge-default', 'badge-default'),
        ('badge-primary', 'badge-primary'),
        ('badge-secondary', 'badge-secondary'),
        ('badge-success', 'badge-success'),
        ('badge-danger', 'badge-danger'),
        ('badge-warning', 'badge-warning'),
        ('badge-info', 'badge-info'),
        ('badge-light', 'badge-light'),
        ('badge-dark', 'badge-dark')
    )

    tag = models.CharField(max_length=12)
    color = models.CharField(choices=CHOICES, max_length=20)

    def __str__(self):
        return self.tag


class ItemCategory(models.Model):
    name = models.CharField(max_length=30)
    img = models.ImageField(upload_to='item/category/img/',
                            blank=True, default=DEFAULT_IMG)

    def __str__(self):
        return self.name
