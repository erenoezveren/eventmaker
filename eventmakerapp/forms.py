from django import forms
from eventmakerapp.models import Comment, UserProfile
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
    entry = forms.CharField(initial='Enter Country, City or Street', required=False)

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('first_name', 'last_name', 'picture', 'description', 'is_business')
