# Generated by Django 2.2.8 on 2020-03-29 04:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_auto_20200329_0404'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='category',
            field=models.CharField(choices=[('S', 'Shirts'), ('SW', 'Sport Wears'), ('O', 'Outwears'), ('A', 'Accessories')], max_length=2),
        ),
    ]
