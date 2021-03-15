
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

from eventmakerapp.models import Event
from eventmakerapp.forms import EventForm

# Create your views here.
def index(request):
    #Home page
    
    Popular_Events = Event.objects.order_by("-likes")[:5]
    More_Events = Event.objects.order_by("-likes")[:5]
    Nearby_Events = Event.objects.extra(where=["location='glasgow'"])
    
    context_dict = {}
    context_dict["popular"] = Popular_Events
    context_dict["more"] = More_Events
    context_dict["near"] = Nearby_Events
    
    response = render(request, 'eventmaker/index.html',context=context_dict)
    return response
    
def about(request):
    #about page view
    
    context_dict = {}
    
    response = render(request, 'eventmaker/about.html',context=context_dict) 
    return response
    
def register(request):

    return