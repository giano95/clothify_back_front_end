# Generated by Django 2.2.8 on 2020-04-15 01:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_auto_20200414_2321'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='country',
            name='continent',
        ),
        migrations.RemoveField(
            model_name='location',
            name='continent',
        ),
        migrations.RemoveField(
            model_name='location',
            name='country',
        ),
        migrations.DeleteModel(
            name='Continent',
        ),
        migrations.DeleteModel(
            name='Country',
        ),
        migrations.DeleteModel(
            name='Location',
        ),
    ]
