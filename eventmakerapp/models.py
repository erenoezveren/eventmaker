from django.db import models

class User(models.Model):
    is_business = models.BooleanField(default=False)
    username = models.CharField(max_length=64)
    email = models.EmailField(max_length=64, blank=True)
    description = models.TextField(blank=True)
    picture = models.ImageField(blank=True)
    website = models.URLField(max_length=64, blank=True)

    def __str__(self):
        return self.name

class Event(models.Model):
    title = models.CharField(max_length=32)
    location = models.CharField(max_length=128, blank=True)
    picture = models.ImageField(blank=True)
    time = models.DateTimeField(blank=True)
    price = models.IntegerField(blank=True)
    likes = models.ManyToManyField(User, related_name="liked", blank=True)
    amount_likes = models.IntegerField(default=0, null=False)
    joins = models.ManyToManyField(User, related_name="joined", blank=True)
    comments = models.ManyToManyField(User, related_name="commented", through='Comment', blank=True)
    host = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.title

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    data = models.TextField()

    def __str__(self):
        return self.data
