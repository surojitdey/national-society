# Generated by Django 3.1.7 on 2022-01-24 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('society', '0002_auto_20220120_1111'),
    ]

    operations = [
        migrations.AddField(
            model_name='society',
            name='registration_number',
            field=models.CharField(default='', max_length=50, verbose_name='registration number'),
        ),
    ]
