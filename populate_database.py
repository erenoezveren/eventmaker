import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'eventmaker.settings')
import django
import datetime
from django.utils import timezone
import pytz

from django import forms

django.setup()

from eventmakerapp.models import UserProfile, Event, Comment    
from django.contrib.auth.models import User         


def populate():
    
    #Populate Users 
    Users = {"first_name":["John","Cara","Bill","Matthew","Kira","Charlie","Euan","Emma","Ben","Jamie"],
             "last_name" :["Smith","johnson","Williams","Brown","Jones","Miller","Davis","Hunter","Rodriguez","Martinez"],
             "is_business":[True,True,True,False,False,False,False,False,False,False],
             "description":["","","","","","","","","","",],
             "picture":[None,None,None,None,None,None,None,None,None,None],}
            
    for i in range(10):
        
        #create or get User built into django
        user, created = User.objects.get_or_create(username=Users["first_name"][i])
        #fore make password for testing purpose 
        user.set_password('pass' + Users["first_name"][i])
        user.save()
        
        #call funtion to make the Userprofile in custom model
        UserProfile = add_User(user,
        Users["first_name"][i],
        Users["last_name"][i],
        Users["is_business"][i],
        Users["description"][i],
        Users["picture"][i])
        
        
    #Populate Events 
    Date = [datetime.datetime(2021, 7, 2, 18, 0, 0, 0,tzinfo=pytz.UTC),
            datetime.datetime(2021, 4, 29, 19, 0, 0, 0,tzinfo=pytz.UTC),
            datetime.datetime(2021, 5, 1, 20, 0, 0, 0,tzinfo=pytz.UTC),
            datetime.datetime(2021, 7, 29, 19, 0, 0, 0,tzinfo=pytz.UTC),
            datetime.datetime(2021, 2, 12, 18, 0, 0, 0,tzinfo=pytz.UTC),
            datetime.datetime(2021, 1, 3, 18, 0, 0, 0,tzinfo=pytz.UTC),
            datetime.datetime(2021, 7, 21, 12, 0, 0, 0,tzinfo=pytz.UTC),
            datetime.datetime(2021, 7, 1, 18, 0, 0, 0,tzinfo=pytz.UTC),
            datetime.datetime(2021, 3, 29, 15, 0, 0, 0,tzinfo=pytz.UTC),
            datetime.datetime(2021, 12, 23, 13, 0, 0, 0,tzinfo=pytz.UTC),
            ]
                
    description = ["","","","","","","","","","", ] 

    
    hosts = ["John","Cara","Bill","John","Cara","Bill","John","Cara","Bill","John",]
    Eventhosts = [] 
    for i in range(10):
        user = User.objects.get(username=hosts[i])
        Eventhosts.append(user)
        
    
    Events = {  "title":["Hive Thursday", "MCFLY", "NICK CAVE AND THE BAD SEEDS", "Music Show", "Open Mic Night", "Happy Hour", "Chess Tournement", "Highland Ceilidh", "Fun Run" , "Liiter Picking in Kelvingrove Park"],
                "description": description,
                "entry":["", "", "", "", "", "", "", "", "", "", ],
                "location":["55.872530, -4.284912", "55.860044, -4.285217", "55.860044, -4.285217", "55.860044, -4.285217", "55.874865, -4.292925", "55.874865, -4.292925", "55.871796, -4.288292", "55.871483, -4.288543", "55.858129, -4.254747", "55.867991, -4.283774",],
                "picture":[None, None, None, None, None, None, None, None, None, None, ],
                "time": Date,
                "price":[4, 25, 40, 3, 0, 0, 6, 5, 5, 0],                
                "amount_likes":[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ],              
                "host":Eventhosts}
    
        
    for i in range(10):
        add_event(  Events["title"][i],
                    Events["description"][i],
                    Events["entry"][i],
                    Events["location"][i],
                    Events["picture"][i],
                    Events["time"][i],
                    Events["price"][i],               
                    Events["amount_likes"][i],           
                    Events["host"][i],
                    )

#create user in database
def add_User(user,first_name,last_name,is_business,description,picture=None):
    U = UserProfile.objects.get_or_create(
    user=user,
    first_name=first_name,
    last_name=last_name,
    is_business=is_business)
    
    
def add_event(title,description,entry,location,picture,time,price,amount_likes,host): 

    E = Event.objects.get_or_create(   
    title=title,
    description=description,
    entry=entry,
    location=location,
    picture=picture,
    time=time,
    price=price,   
    amount_likes=amount_likes,
    host=host)
    
   
   
def add_comment():
    pass


if __name__ == '__main__':  
    print("Population Eventmaker with population script...")
    populate()
        