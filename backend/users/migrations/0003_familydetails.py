# Generated by Django 3.1.7 on 2021-02-28 19:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_role'),
    ]

    operations = [
        migrations.CreateModel(
            name='FamilyDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('relation', models.CharField(choices=[('husband', 'husband'), ('wife', 'wife'), ('father', 'father'), ('mother', 'mother'), ('son', 'son'), ('daughter', 'daughter'), ('other', 'other')], default='other', max_length=50, verbose_name='type of relation')),
                ('member_name', models.CharField(max_length=50, verbose_name='family member name')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
