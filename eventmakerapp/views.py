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

from django.contrib.auth.models import User

from eventmakerapp.forms import CommentForm, Address, UserForm, UserProfileForm, EventForm, AddressEvent

from django.http import HttpResponseRedirect
# Create your views here.
def index(request):

    return index_helper(request, None, None)

def about(request):
    #about page view
    
    context_dict = {}
    Popular_Events = Event.objects.order_by("-amount_likes")[:1]  
    context_dict["popular"] = Popular_Events
    User_Profiles = UserProfile.objects.all()
    context_dict["user_profiles"] = User_Profiles
    
    response = render(request, 'eventmaker/about.html', context=context_dict)
    return response
    
    
def show_event(request, event_name):    
    context_dict = {}



    User_Profiles = UserProfile.objects.all()
    context_dict["user_profiles"] = User_Profiles
    #get comments
    try:
        eventObj = Event.objects.get(title=event_name)
        commentsObj = Comment.objects.filter(event = eventObj)
        
        context_dict["event"] = eventObj 
        context_dict["comments"] = commentsObj

        form = Address(initial={"location": eventObj.location})
        context_dict["form"] = form
        
    except Event.DoesNotExist:
        context_dict["title"] = None 
        context_dict["comments"] = None

    return render(request, 'eventmaker/event.html', context=context_dict)
    
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
    User_Profiles = UserProfile.objects.all()
    context_dict["user_profiles"] = User_Profiles
    
    try:
        eventObj = Event.objects.get(title=event_name)
        commentsObj = Comment.objects.filter(event = eventObj)
        userobj = User.objects.get(id=request.user.id)
                                                        
        
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


def checkLocation(request):


    if request.method == 'POST':
        form = Address(request.POST)

        if form.is_valid():

            coordinates = form.cleaned_data.get('location')
            x,y = coordinates.split(",")

            distances = []
            for event in Event.objects.all():
                coordinatesEvent = event.location

                xE,yE = coordinatesEvent.split(",")
                distances.append((event, math.sqrt(((float(x) - float(xE)) ** 2) + (float(y) - float(yE)) ** 2)))

            distances.sort(key=lambda elem: elem[1])

            Nearby_Events = [elem[0] for elem in distances][:6]

            return index_helper(request, Nearby_Events, form)

    return redirect(index(request))

def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

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
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('eventmakerapp:index'))
            else:
                return HttpResponse("Your account is disabled.")
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'eventmaker/login.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('eventmakerapp:index'))


def userProfile(request, user_name):
    context_dict = {}

    User_Profiles = UserProfile.objects.all()
    context_dict["user_profiles"] = User_Profiles

    try:
        userobj = User.objects.get(username=user_name)
        userProfileobj = UserProfile.objects.get(user__username__exact=user_name)
        liked = userobj.liked.all()[:6]


        context_dict["userProfile"] = userProfileobj
        context_dict["user"] = userobj
        context_dict["events"] = liked


    except User.DoesNotExist:
        context_dict["user"] = None
        context_dict["userProfile"] = None
        context_dict["events"] = None

    except UserProfile.DoesNotExist:
        context_dict["user"] = None
        context_dict["userProfile"] = None
        context_dict["events"] = None
    return render(request, 'eventmaker/user_profile.html', context_dict)

#like view
@login_required
def like_event(request, event_name):
    post = get_object_or_404(Event, id = request.POST.get('like_button'))
    post.liked.add(request.user)
    
    return redirect(reverse('eventmakerapp:show_event', kwargs={'event_name':event_name}))  

@login_required
def join_event(request, event_name):
    post = get_object_or_404(Event, id = request.POST.get('join_button'))

    return redirect(reverse('eventmakerapp:show_event', kwargs={'event_name':event_name}))

@login_required
def addEvent(request):

    form = EventForm()

    if request.method == 'POST':
        form = EventForm(request.POST)

        if form.is_valid():
            event_instance = form.save(commit=False)
            event_instance.host = request.user
            event_instance.save()

            return redirect('/eventmaker/')

        else:
            print(form.errors)

    return render(request, 'eventmaker/addEvent.html', {'form': form})
