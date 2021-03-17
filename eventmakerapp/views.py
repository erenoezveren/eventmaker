from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth import logout
from eventmakerapp.models import Event
from eventmakerapp.models import Comment

# Create your views here.
def index(request):
    #Home page
    
    Popular_Events = Event.objects.order_by("-amount_likes")[:5]
    More_Events = Event.objects.order_by("-title")[:5] #can be changed to other form of sorting 
    Nearby_Events = Event.objects.extra(where=["location='Glasgow'"])[:5] #Need to get users location 
    
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
    
    
def show_event(request, event_name):    
    context_dict = {}
    
    try:
        eventObj = Event.objects.get(title=event_name)
        commentsObj = Comment.objects.filter(event = eventObj)
        
        context_dict["event"] = eventObj 
        context_dict["comments"] = commentsObj
        
    except Event.DoesNotExist:
        context_dict["title"] = None 
        context_dict["comments"] = None
    
    return render(request, 'eventmaker/event.html', context=context_dict)

        