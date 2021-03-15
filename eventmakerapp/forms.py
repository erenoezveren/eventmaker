from django import forms
from eventmakerapp.models import Event, User, BusinessProfile, UserProfile
from django.contrib.auth.models import User


class EventForm(forms.ModelForm):
    title = forms.CharField(max_length=32)
    location = forms.CharField(max_length=128)
    picture = forms.ImageField()
    time = forms.DateTimeField()
    price = forms.IntegerField()
    
    class Meta:
        model = Event
        fields = ("title", "location", "picture", "time", "price",)
        
class UserForm(forms.ModelForm):
    name = forms.CharField(max_length=64)
    email = forms.EmailField(max_length=64)
    description = forms.CharField(max_length=1024)
    picture = forms.ImageField()
    
    class Meta:
        model = User
        fields = ('name', 'email', 'description', 'picture')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = '__all__'
        
class BusinessProfileForm(forms.ModelForm):
    class Meta:
        model = BusinessProfile
        fields = ('website',)

