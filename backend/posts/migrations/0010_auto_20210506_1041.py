# Generated by Django 3.1.7 on 2021-05-06 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0009_complaintsandgrievances_solution_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='description',
            field=models.TextField(blank=True, max_length=20000, verbose_name='description'),
        ),
    ]
