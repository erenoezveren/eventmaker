# Generated by Django 2.2.17 on 2021-03-21 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventmakerapp', '0002_auto_20210321_1737'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='first_name',
            field=models.CharField(default=False, max_length=18),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='last_name',
            field=models.CharField(default=False, max_length=18),
        ),
    ]