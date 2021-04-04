from django.shortcuts import render

from eventmakerapp.forms import Address
from eventmakerapp.models import Event, UserProfile

def index_helper(request, nearby, form):
    # Home page
    context_dict = {}

    if nearby and form:
        context_dict["near"] = nearby
        context_dict["form"] = form
    else:
        form = Address()
        context_dict["form"] = form

    # Find popular Events
    Popular_Events = Event.objects.all()      
    Popular_Events = sorted(Popular_Events, key = lambda t : t.total_likes(), reverse=True)[:6]
    
    # remove already displayed events
    More_Events = Event.objects.all()
   
    DeleteList = []
    for E in More_Events:
        for popE in Popular_Events:
            if E.title == popE.title:
                DeleteList.append(E.id)

    More_Events = More_Events.filter().exclude(id__in=DeleteList)
    User_Profiles = UserProfile.objects.all()
    context_dict["user_profiles"] = User_Profiles

    context_dict["popular"] = Popular_Events
    context_dict["more"] = More_Events


    response = render(request, 'eventmaker/index.html', context=context_dict)
    return response

