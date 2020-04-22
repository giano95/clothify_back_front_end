# Generated by Django 2.2.8 on 2020-04-22 04:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20200422_0229'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='img',
            field=models.ImageField(blank=True, default='https://mdbootstrap.com/img/Photos/Horizontal/E-commerce/Vertical/15.jpg', upload_to=''),
        ),
        migrations.AlterField(
            model_name='item',
            name='unit',
            field=models.CharField(choices=[('stock', 'STOCK'), ('each', 'EACH')], default='each', max_length=80),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_type',
            field=models.CharField(choices=[('Buyer', 'Buyer'), ('Seller', 'Seller')], max_length=10),
        ),
    ]
