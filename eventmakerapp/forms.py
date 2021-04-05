from django import forms
from eventmakerapp.models import Comment, UserProfile, Event
from location_field.forms.plain import PlainLocationField
from django.contrib.auth.models import User

class CommentForm(forms.ModelForm):
    #Comment for to make new comments
    #data is filled by the post request and user and event are added after its created 
    data = forms.CharField(help_text="Enter Comment, can't be black or longer that 256 chars")
    
    class Meta:
        model = Comment
        exclude = ('user', 'event')
        
        
class Address(forms.Form):
    #to get location on the map
    location = PlainLocationField(based_fields=['entry'],
                                  initial='55.8719,-4.2883')
    entry = forms.CharField(required=False)


class UserForm(forms.ModelForm):
    #create new user, password is passed in encrypted 
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)

class UserProfileForm(forms.ModelForm):
    #to create new userProfile 
    class Meta:
        model = UserProfile
        fields = ('first_name', 'last_name', 'picture', 'description', 'is_business')

class EventForm(forms.ModelForm):
    #to create new event, contains help text to display on page 

    title = forms.CharField(help_text="Enter an event title")
    description = forms.CharField(help_text="Enter a description")
    locationName = forms.CharField(help_text="Enter the name of the venue")
    location = PlainLocationField(based_fields=['entry'],
                                  initial='0,0')
    entry = forms.CharField(help_text="Enter an address here or pick a location from the map", required=False)
    host = forms.HiddenInput()
    picture = forms.ImageField(help_text="Upload a picture", required=False)
    time = forms.DateTimeField(help_text="Pick a time", input_formats=['%d/%m/%Y %H:%M'])
    price = forms.CharField(help_text="Enter a price")

    class Meta:
        model = Event
        fields = ('title', 'description', 'location', 'entry', 'locationName', 'picture', 'time', 'price')


