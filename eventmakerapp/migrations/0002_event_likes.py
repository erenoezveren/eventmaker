# Generated by Django 2.2.17 on 2021-04-04 13:26

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('eventmakerapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='liked', through='eventmakerapp.Like', to=settings.AUTH_USER_MODEL),
        ),
    ]
