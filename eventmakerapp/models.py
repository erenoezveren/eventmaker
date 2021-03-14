from django.contrib.auth.models import AbstractUser
from django.db import models

class Account(models.Model):
    is_business = models.BooleanField()
    name = models.CharField(max_length=64, null=False)
    email = models.EmailField(max_length=64)
    description = models.TextField()
    picture = models.ImageField()

    def __str__(self):
        return self.name

class Business(models.Model):
    account = models.OneToOneField(Account, on_delete=models.CASCADE, primary_key=True, default="")
    website = models.URLField(max_length=64)

    class Meta:
        verbose_name_plural = 'Businesses'


class Event(models.Model):
    title = models.CharField(max_length=32, null=False)
    location = models.CharField(max_length=128, null=False)
    picture = models.ImageField()
    time = models.DateTimeField()
    price = models.IntegerField()
    host = models.ForeignKey(
        Business,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.title

class User(models.Model):
    account = models.OneToOneField(Account, on_delete=models.CASCADE, primary_key=True, default="")
    likes = models.ManyToManyField(Event, related_name="likes")
    joins = models.ManyToManyField(Event, related_name="joins")
    comments = models.ManyToManyField(Event, related_name="comments", through='Comment')



class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    data = models.TextField(null=False)

    def __str__(self):
        return self.data