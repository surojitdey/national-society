# Generated by Django 3.1.7 on 2021-07-17 13:10

from django.db import migrations, models
import posts.models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0011_auto_20210506_1041'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='thumbnail',
            field=models.FileField(blank=True, upload_to=posts.models.user_thumbnail_directory_path),
        ),
    ]
