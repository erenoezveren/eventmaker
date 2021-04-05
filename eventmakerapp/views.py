import math

from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from eventmakerapp.functions import index_helper
from eventmakerapp.models import Event
from eventmakerapp.models import Comment
from eventmakerapp.models import UserProfile
from eventmakerapp.models import Like

from django.contrib.auth.models import User

from eventmakerapp.forms import CommentForm, Address, UserForm, UserProfileForm, EventForm

from django.http import HttpResponseRedirect
# Create your views here.
def index(request):
    #uses function from functions
    return index_helper(request, None, None)

def about(request):
    #about page view
    
    context_dict = {}
    #gets 1 querylist with 1 event
    Popular_Events = Event.objects.order_by("title")[:1]  
    User_Profiles = UserProfile.objects.all()
    
    #passes to context dict for template 
    context_dict["popular"] = Popular_Events
    context_dict["user_profiles"] = User_Profiles
    
    response = render(request, 'eventmaker/about.html', context=context_dict)
    return response
    
    
def show_event(request, event_name):    
    context_dict = {}

    #get comments
    try:
        #gets event from event_name passed from page, and comments 
        eventObj = Event.objects.get(title=event_name)
        commentsObj = Comment.objects.filter(event = eventObj)
        
        #passes to context dict to pass to page 
        context_dict["event"] = eventObj 
        context_dict["comments"] = commentsObj

        #form to display event location on map 
        form = Address(initial={"location": eventObj.location})
        context_dict["form"] = form
        
        #handle errors 
    except Event.DoesNotExist:
        context_dict["event"] = None 
        context_dict["comments"] = None
        context_dict["form"] = None
        
    return render(request, 'eventmaker/event.html', context=context_dict)
    
    
@login_required  
def LikeView(request, pk):

    #get event obj from pk passed from page 
    post = get_object_or_404(Event, id=request.POST.get('event_id'))
    #add new entry to table in many to many relation 
    post.likes.add(request.user)
    
    #Redirects to same page to reload it 
    return HttpResponseRedirect(reverse('eventmakerapp:show_event', kwargs={'event_name':post.title}))
    
    
    
def eventsearch(request):

    context_dict = {}
    #get value of search box from the request and seach box name
    query = request.GET.get('searchEvent')
    User_Profiles = UserProfile.objects.all()
    context_dict["user_profiles"] = User_Profiles
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
     
    try:
        #gets event and user objects to pass to form to make new entry in table
        eventObj = Event.objects.get(title=event_name) 
        userobj = User.objects.get(id=request.user.id)
        
        context_dict["event"] = eventObj 
        
    #handle errors
    except Event.DoesNotExist:
        context_dict["event"] = None 
        context_dict["comments"] = None
        
     
    comment_form = CommentForm()
    newComment = None
    
    if request.method == 'POST':
        #create comment obj from form with the data 
        comment_form = CommentForm(request.POST)
        
        if comment_form.is_valid():
            #if obj is valid add the info about the user and event
            newComment = comment_form.save(commit=False)
            newComment.event = eventObj
            newComment.user = userobj
            #save comment
            newComment.save()

            return redirect(reverse('eventmakerapp:show_event', kwargs={'event_name':event_name}))
            
        else:
            print(comment_form.is_valid())
    
    #form for data entry on page 
    context_dict['form'] = comment_form
    
    return render(request, 'eventmaker/makecomment.html', context=context_dict)


def checkLocation(request):

    #to get nearby events 
    if request.method == 'POST':
        #form for the location
        form = Address(request.POST)

        if form.is_valid():

            coordinates = form.cleaned_data.get('location')
            x,y = coordinates.split(",")

            distances = []
            
            #works out distance from location on map to event for each event
            for event in Event.objects.all():
                coordinatesEvent = event.location

                xE,yE = coordinatesEvent.split(",")
                distances.append((event, math.sqrt(((float(x) - float(xE)) ** 2) + (float(y) - float(yE)) ** 2)))
            #get the closest events 
            distances.sort(key=lambda elem: elem[1])

            
            Nearby_Events = [elem[0] for elem in distances][:6]

            #call index helper with new information on neaby events to update page 
            return index_helper(request, Nearby_Events, form)

    return redirect(index(request))

def register(request):
    registered = False

    #register new user 
    if request.method == 'POST':
        #get forms to create new obj for user and UserProfile
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        #if valid set password and save, make user then make UserProfile with the new user 
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            
            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'eventmaker/register.html', context={'user_form': user_form, 'profile_form': profile_form, 'registered': registered})

def user_login(request):

    if request.method == 'POST':
        #get input from html forms post request 
        username = request.POST.get('username')
        password = request.POST.get('password')

        #check username and password are valid 
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                #login and go to home page 
                login(request, user)
                return redirect(reverse('eventmakerapp:index'))
            else:
                #if user account has been disabled by admins etc.
                return HttpResponse("Your account is disabled.")
        else:
            #password/username do not match
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'eventmaker/login.html')

@login_required
def user_logout(request):
    #log user out and go to home page 
    logout(request)
    return redirect(reverse('eventmakerapp:index'))


def userProfile(request, user_name):
    context_dict = {}

    #get userprofiles  
    User_Profiles = UserProfile.objects.all()
    context_dict["user_profiles"] = User_Profiles

    try:
        #get user and userProfile obj
        userobj = User.objects.get(username=user_name)
        userProfileobj = UserProfile.objects.get(user__username__exact=user_name)
        liked = userobj.liked.all()

        #pass to context dict for page 
        context_dict["userProfile"] = userProfileobj
        context_dict["userOther"] = userobj
        context_dict["events"] = liked

    #handle errors 
    except User.DoesNotExist:
        context_dict["userOther"] = None
        context_dict["userProfile"] = None
        context_dict["events"] = None

    except UserProfile.DoesNotExist:
        context_dict["userOther"] = None
        context_dict["userProfile"] = None
        context_dict["events"] = None
    return render(request, 'eventmaker/user_profile.html', context_dict)



@login_required
def addEvent(request):

    #get event form to create new event obj
    form = EventForm()

    if request.method == 'POST':
        form = EventForm(request.POST)

        if form.is_valid():
            #if form is valid from info from past then add the current user as the host and save 
            event_instance = form.save(commit=False)
            event_instance.host = request.user
            event_instance.save()

            return redirect('/eventmaker/')

        else:
            print(form.errors)

    return render(request, 'eventmaker/addEvent.html', {'form': form})
