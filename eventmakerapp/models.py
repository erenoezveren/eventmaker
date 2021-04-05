from django.db import models
from location_field.models.plain import PlainLocationField
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=32, blank=False, default="")
    last_name = models.CharField(max_length=20, blank=False, default="")
    is_business = models.BooleanField("Do you represent a business?", default=False)
    description = models.TextField("About you", blank=True)
    picture = models.ImageField("Profile picture", default='defaultProfilePic.jpg')

    def __str__(self):
        return self.user.username

class Event(models.Model):
    title = models.CharField(max_length=32)
    description = models.TextField()   
    locationName = models.TextField(max_length=64, blank=True)##   
    entry = models.CharField(max_length=255, blank=True)
    location = PlainLocationField(based_fields=['entry'], zoom=7, blank=True)
    picture = models.ImageField(default='NoEventImage.png')
    time = models.DateTimeField(null=True)
    price = models.FloatField(null=True)
    likes = models.ManyToManyField(User, related_name="liked", blank=True, through="Like")    
    comments = models.ManyToManyField(User, related_name="commented", through='Comment', blank=True)
    host = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    
    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.title

class Comment(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    data = models.TextField()

    def __str__(self):
      return self.data
      
class Like(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.event.title + " " + self.user.username

