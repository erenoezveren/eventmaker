from django import forms
from eventmakerapp.models import Comment, Place
from location_field.forms.plain import PlainLocationField


class CommentForm(forms.ModelForm):
    
    data = forms.CharField(help_text="Enter Comment, can't be black or longer that 256 chars")
    
    class Meta:
        model = Comment
        exclude = ('user', 'event')

class Address(forms.Form):

    location = PlainLocationField(based_fields=['entry'],
                                  initial='55.8719,-4.2883')
    entry = forms.CharField(initial='University of Glasgow')

