from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_business', models.BooleanField(default=False)),
                ('username', models.CharField(max_length=64)),
                ('email', models.EmailField(blank=True, max_length=64)),
                ('description', models.TextField(blank=True)),
                ('picture', models.ImageField(blank=True, upload_to='')),
                ('website', models.URLField(blank=True, max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32)),
                ('location', models.CharField(blank=True, max_length=128)),
                ('picture', models.ImageField(blank=True, upload_to='')),
                ('time', models.DateTimeField(blank=True)),
                ('price', models.IntegerField(blank=True)),
                ('amount_likes', models.IntegerField(default=0)),
                ('comments', models.ManyToManyField(blank=True, related_name='commented', through='eventmakerapp.Comment', to='eventmakerapp.User')),
                ('host', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eventmakerapp.User')),
                ('joins', models.ManyToManyField(blank=True, related_name='joined', to='eventmakerapp.User')),
                ('likes', models.ManyToManyField(blank=True, related_name='liked', to='eventmakerapp.User')),
            ],
        ),
        migrations.AddField(
            model_name='comment',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eventmakerapp.Event'),
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eventmakerapp.User'),
        ),
    ]
