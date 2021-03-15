from django import forms
from eventmakerapp.models import Event, User

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
    username = forms.CharField(max_length=64)
    email = forms.EmailField(max_length=64)
    description = forms.CharField(max_length=1024)
    picture = forms.ImageField()
    website = forms.URLField(max_length=64)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'description', 'picture', 'website',)

