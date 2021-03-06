# Generated by Django 3.1.7 on 2021-08-25 08:39

from django.db import migrations, models
import security.models


class Migration(migrations.Migration):

    dependencies = [
        ('security', '0003_auto_20210825_0825'),
    ]

    operations = [
        migrations.AlterField(
            model_name='security',
            name='adhar_card_thumbnail',
            field=models.FileField(blank=True, upload_to=security.models.security_thumbnail_directory_path),
        ),
        migrations.AlterField(
            model_name='security',
            name='photo_thumbnail',
            field=models.FileField(blank=True, upload_to=security.models.security_thumbnail_directory_path),
        ),
    ]
