# Generated by Django 3.1.7 on 2021-04-21 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ContactDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('community_name', models.CharField(blank=True, max_length=100, verbose_name='community name')),
                ('appartment_name', models.CharField(blank=True, max_length=100, verbose_name='appartment name')),
                ('address_one', models.CharField(blank=True, max_length=200, verbose_name='address one')),
                ('address_two', models.CharField(blank=True, max_length=200, verbose_name='address two')),
                ('city', models.CharField(blank=True, max_length=200, verbose_name='city')),
                ('pincode', models.CharField(blank=True, max_length=6, verbose_name='pincode')),
                ('contact_number', models.CharField(blank=True, max_length=13, verbose_name='contact number')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('show_address', models.BooleanField(default=False, verbose_name='show address')),
                ('show_number', models.BooleanField(default=False, verbose_name='show contact number')),
                ('show_email', models.BooleanField(default=False, verbose_name='show email-id')),
            ],
        ),
    ]
