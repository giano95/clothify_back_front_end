# Generated by Django 2.2.8 on 2020-04-22 05:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20200422_0450'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='connected_account_id',
            field=models.TextField(blank=True, null=True),
        ),
    ]
