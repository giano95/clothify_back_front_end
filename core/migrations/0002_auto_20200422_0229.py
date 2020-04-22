# Generated by Django 2.2.8 on 2020-04-22 02:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='item',
            name='unit',
            field=models.CharField(blank=True, choices=[('stock', 'STOCK'), ('each', 'EACH')], default='each', max_length=80, null=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='img',
            field=models.ImageField(blank=True, default='https://mdbootstrap.com/img/Photos/Horizontal/E-commerce/Vertical/15.jpg', upload_to='media'),
        ),
        migrations.DeleteModel(
            name='Profile',
        ),
    ]