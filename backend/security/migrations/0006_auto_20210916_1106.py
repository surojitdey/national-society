# Generated by Django 3.1.7 on 2021-09-16 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('security', '0005_timetable'),
    ]

    operations = [
        migrations.AddField(
            model_name='timetable',
            name='task_day',
            field=models.CharField(choices=[('all', 'all'), ('mon', 'mon'), ('tue', 'tue'), ('wed', 'wed'), ('thu', 'thu'), ('fri', 'fri'), ('sat', 'sat'), ('sun', 'sun')], default='all', max_length=3, verbose_name='task day'),
        ),
        migrations.AlterField(
            model_name='timetable',
            name='task_date',
            field=models.DateField(blank=True),
        ),
    ]
