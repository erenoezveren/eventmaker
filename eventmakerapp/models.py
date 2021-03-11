from django.db import models

class Business(models.Model):
    id = models.CharField(max_length=32, unique=True)
    name = models.CharField(max_length=64)
    #Password:
    email = models.EmailField(max_length=64)
    description = models.TextField()
    picture = models.ImageField()

    def __str__(self):
        return self.name

class Event(models.Model):
    id = models.CharField(max_length=32, unique=True)
    title = models.CharField(max_length=32)
    location = models.CharField(max_length=128)
    picture = models.ImageField()
    time = models.TimeField()
    price = models.IntegerField()

    def __str__(self):
        return self.title


class User(models.Model):
    id = models.CharField(max_length=32, unique=True)
    username = models.CharField(max_length=64)
    # Password:
    email = models.EmailField(max_length=64)
    bio = models.TextField()
    picture = models.ImageField()

    def __str__(self):
        return self.name

class Comment(models.Model):
    id = models.CharField(max_length=64, unique=True)
    data = models.TextField()
