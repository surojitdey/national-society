# Generated by Django 3.1.7 on 2021-06-29 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20210621_1955'),
    ]

    operations = [
        migrations.AddField(
            model_name='otp',
            name='otp_type',
            field=models.CharField(choices=[('password', 'password'), ('forgot_password', 'forgot_password'), ('number_change', 'number_change'), ('signup', 'signup')], default='signup', max_length=50, verbose_name='otp type'),
        ),
    ]
