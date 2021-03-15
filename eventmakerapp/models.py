from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    is_business = models.BooleanField(default=False)
    name = models.CharField(max_length=64, null=False)
    email = models.EmailField(max_length=64, default=False)
    description = models.TextField(null=True)
    picture = models.ImageField(null=True)

    def __str__(self):
        return self.name

class BusinessProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='business_profile', primary_key=True)
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
        BusinessProfile,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.title

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile', primary_key=True)
    likes = models.ManyToManyField(Event, related_name="likes")
    joins = models.ManyToManyField(Event, related_name="joins")
    comments = models.ManyToManyField(Event, related_name="comments", through='Comment')

def create_user_profile(sender, instance, created, **kwargs):
    print('****', created)
    if instance.is_business:
        BusinessProfile.objects.get_or_create(user = instance)
    else:
        UserProfile.objects.get_or_create(user = instance)
        
def save_user_profile(sender, instance, **kwargs):
	print('_-----')	
	if instance.is_business:
		instance.business_profile.save()
	else:
		UserProfile.objects.get_or_create(user = instance)


class Comment(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    data = models.TextField(null=False)

    def __str__(self):
        return self.data