from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

from eventmakerapp.models import Event
from eventmakerapp.models import Comment
from eventmakerapp.models import User

from eventmakerapp.forms import CommentForm

# Create your views here.
def index(request):
    #Home page
    context_dict = {}
     
    Popular_Events = Event.objects.order_by("-amount_likes")[:5]  
    Nearby_Events = Event.objects.extra(where=["location='Glasgow'"])[:5] #Need to get users location 
    More_Events = Event.objects.order_by("-title")[:5] #can be changed to other form of sorting 
   
    context_dict["popular"] = Popular_Events
    context_dict["near"] = Nearby_Events
    context_dict["more"] = More_Events
     
    response = render(request, 'eventmaker/index.html',context=context_dict)
    return response
    
def about(request):
    #about page view
    
    context_dict = {}
    
    response = render(request, 'eventmaker/about.html',context=context_dict) 
    return response
    
    
def show_event(request, event_name):    
    context_dict = {}
     
    #get comments
    try:
        eventObj = Event.objects.get(title=event_name)
        commentsObj = Comment.objects.filter(event = eventObj)
        
        context_dict["event"] = eventObj 
        context_dict["comments"] = commentsObj
        
    except Event.DoesNotExist:
        context_dict["title"] = None 
        context_dict["comments"] = None
      
    return render(request, 'eventmaker/event.html', context=context_dict)
    
def eventsearch(request):

    context_dict = {}
    #get value of search box from the request and seach box name
    query = request.GET.get('searchEvent')
    
    try:
        #genral search in database for similar titles
        eventObj = Event.objects.filter(title__contains = query)
        context_dict["searches"] = eventObj
        context_dict["SearchValue"] = query
        
    except Event.DoesNotExist:
        context_dict["searches"] = None
        context_dict["SearchValue"] = None

    return render(request, 'eventmaker/eventsearch.html', context=context_dict)
    
@login_required 
def makecomment(request, event_name):
    context_dict = {}
    
    print(request.user)
    
    try:
        eventObj = Event.objects.get(title=event_name)
        commentsObj = Comment.objects.filter(event = eventObj)
        userobj = User.objects.get(id=request.user.id) #User account is not in the database 
                                                        #so cant get the correct one
        
        context_dict["event"] = eventObj 
        context_dict["comments"] = commentsObj
        
    except Event.DoesNotExist:
        context_dict["event"] = None 
        context_dict["comments"] = None
        
     
    comment_form = CommentForm()
    newComment = None
    
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        
        if comment_form.is_valid():
            newComment = comment_form.save(commit=False)
            newComment.event = eventObj
            newComment.user = userobj
            newComment.save()
            
            
            return redirect(reverse('eventmakerapp:show_event', kwargs={'event_name':event_name}))
            
        else:
            print(comment_form.is_valid())
    
    context_dict['form'] = comment_form
    
    return render(request, 'eventmaker/makecomment.html', context=context_dict)








        