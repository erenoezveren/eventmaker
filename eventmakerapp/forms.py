from django import forms
from eventmakerapp.models import Comment, UserProfile, Event
from location_field.forms.plain import PlainLocationField
from django.contrib.auth.models import User

class CommentForm(forms.ModelForm):
    
    data = forms.CharField(help_text="Enter Comment, can't be black or longer that 256 chars")
    
    class Meta:
        model = Comment
        exclude = ('user', 'event')

class Address(forms.Form):

    location = PlainLocationField(based_fields=['entry'],
                                  initial='55.8719,-4.2883')
    entry = forms.CharField(required=False)

class AddressEvent(forms.Form):

    location = PlainLocationField(based_fields=None)

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('first_name', 'last_name', 'picture', 'description', 'is_business')

class EventForm(forms.ModelForm):
    title = forms.CharField(help_text="Event title")
    description = forms.CharField(help_text="description")
    location = PlainLocationField(based_fields=['entry'],
                                  initial='0,0')
    entry = forms.CharField(help_text="Enter or pick a location", required=False)
    host = forms.HiddenInput()
    picture = forms.ImageField(help_text="Upload Picture", required=False)
    time = forms.DateTimeField(help_text="Enter a time", input_formats=['%d/%m/%Y %H:%M'])
    price = forms.CharField(help_text="Price")

    class Meta:
        model = Event
        fields = ('title', 'description', 'location', 'entry', 'picture', 'time', 'price')
