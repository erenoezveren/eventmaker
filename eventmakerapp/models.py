from django.db import models

class Business(models.Model):
    name = models.CharField(max_length=64, null=False)
    #Password:
    email = models.EmailField(max_length=64)
    description = models.TextField()
    picture = models.ImageField()
    website = models.URLField(max_length=64)

    def __str__(self):
        return self.name

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
    username = models.CharField(max_length=64, null=False)
    # Password:
    email = models.EmailField(max_length=64)
    bio = models.TextField()
    picture = models.ImageField()
    likes = models.ManyToManyField(Event, related_name="likes")
    joins = models.ManyToManyField(Event, related_name="joins")
    comments = models.ManyToManyField(Event, related_name="comments", through='Comment')

    def __str__(self):
        return self.name

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    data = models.TextField(null=False)

    def __str__(self):
        return self.data