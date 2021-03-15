from django import forms
from eventmakerapp.models import Event

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

