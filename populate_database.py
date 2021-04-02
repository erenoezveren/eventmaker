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
             "description":["Hi everyone! I'm John, an exchange student from Wisconsin, USA. I love taking long hikes in the mountains. Looking forward to having lots of fun in Glasgow!",
                            "Cara here. You can call me C. Did you know that the first oranges weren't actually orange? Studying BioChem second year. Insta: caraJ",
                            "How ye daein?",
                            "'You miss 100% of the shots you don't take. - Wayne Gretzky' - Michael Scott",
                            "Anybody wanna join me for MCFLY on the 29th???? DON'T WANNA GO ALONE",
                            "Hello, my name is Charlie. I am currently studying English Literature. I look forward to joining your event",
                            "",
                            "Favourite colour: Pink. Favourite animal: Fox. Favourite food: Avocado Sushi. Favourite band: Twenty One Pilots",
                            "",
                            "J.Martinez, reporting on deck!",],
             "picture":["images/default.png",None,None,None,None,None,None,None,None,None],}

        
        
    for i in range(10):
        
        #create or get User built into django
        user, created = User.objects.get_or_create(username=Users["first_name"][i])
        #fore make password for testing purpose 
        user.set_password('pass' + Users["first_name"][i])
        user.save()
        
        #call funtion to make the Userprofile in custom model
        add_User(user,
        Users["first_name"][i],
        Users["last_name"][i],
        Users["is_business"][i],
        Users["description"][i])
        
        
    #Populate Events 
    Date = [datetime.datetime(2021, 7, 1, 18, 0, 0, 0,tzinfo=pytz.UTC),
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
            
            
    Pictures = ["Hive.jpg",
                "mcfly.jpg",
                "nick-cave-bad-seeds.jpg",
                "MusicShow.jpeg",
                "karaoke.jpg",
                "Happy-hour.jpg",
                "chess.jpg",
                "Ceilidh.jpg",
                "funrun.jpg",
                "kelvingrove.jpg"]
            
            
            
    #add       
    description = ["Situated in the heart of the West End, Glasgow University Union is a unique venue rich in history. With its grand architecture and original period features, the building boasts a versatility that can see it transformed from a corporate setting into a spectacular and magnificent wedding venue. With the capacity to hold large dinner events, conferences and weddings, at the Glasgow University Union we possess a wealth of knowledge in hosting academic, corporate and private functions. "
    ,"MCFLY at The Hydro. The SSE Hydro is a multi-purpose indoor arena located within the Scottish Event Campus in Glasgow, Scotland. The arena was initially named The Hydro after its main sponsor Scottish Hydro Electric. The arena was officially opened on 30 September 2013, with a concert by Rod Stewart."
    ,"NICK CAVE AND THE BAD SEEDS at the hydro. The SSE Hydro is a multi-purpose indoor arena located within the Scottish Event Campus in Glasgow, Scotland. The arena was initially named The Hydro after its main sponsor Scottish Hydro Electric. The arena was officially opened on 30 September 2013, with a concert by Rod Stewart."
    ,"Some bands playing at our weekly music show"
    ,"Come and give it a go. karaoke night at the Bar"
    ,"All drinks 30% off come down with your friends and have a laugh"
    ,"Amature Chess tournemnt, just have fun"
    ,"Good laugh for everyone, don't need to know any dances just come along"
    ,"Raise Money for charity and get sponsored to do a 5k run!"
    ,"Cleen up the park with us!"
    , ] 

    
    hosts = ["John","Cara","Bill","John","Cara","Bill","John","Cara","Bill","John",]
    Eventhosts = [] 
    for i in range(10):
        #get userobj hosting from username to be the host 
        user = User.objects.get(username=hosts[i])
        Eventhosts.append(user)
        
    
    Events = {  "title":["Hive Thursday", "MCFLY", "NICK CAVE AND THE BAD SEEDS", "Music Show", "Open Mic Night", "Happy Hour", "Chess Tournement", "Highland Ceilidh", "Fun Run" , "Litter Picking in Kelvingrove Park"],
                "description": description,
                "entry":["", "", "", "", "", "", "", "", "", "", ],
                "location":["55.872530, -4.284912", "55.860044, -4.285217", "55.860044, -4.285217", "55.860044, -4.285217", "55.874865, -4.292925", "55.874865, -4.292925", "55.871796, -4.288292", "55.871483, -4.288543", "55.858129, -4.254747", "55.867991, -4.283774",],                
                "picture": Pictures,
                "time": Date,
                "price":[4, 25, 40, 3, 0, 0, 6, 5, 5, 0],                
                "amount_likes":[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ],              
                "host":Eventhosts}
    
    #call add event
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

            
    #All comments None represent no comments left 
    UserComments = {"John" : ["Looks Great!", None, "I am Going next week!", None, "love it!", None, "anyone else going", None, "is this one again next week", None, ]
                    ,"Cara" : [None, "WOW", None, "cant wait", None, "love it", None, "looks amazing!", "Lets go", None, ]
                    ,"Bill" : [None, "Loved this place been before", None, "Never Been but looks good", None, "coming next week", None, "i am bringing everyone", None, ":)", ]
                    ,"Matthew" : ["coming tomorrow", None, "can you bring a bag", None, "whats the phone number for this place", None, "anyone want to come with me?", None, "add me on snap if your going sc_fakeuser", None, ]
                    ,"Kira" : ["is there a locker", None, None, None, None, None, None, None, None, None, ]
                    ,"Charlie" : [None, "is this anygood", "expensive!?", "is there food", None, "can you bring in food", None, "Look so good", None, "great to see this", ]
                    ,"Euan" : ["might come along", None, "I want to do this for my birthday", "can you come early", None, "awesome", None, "Never coming again", None, "WOW", ]
                    ,"Emma" : ["Loved it", None, "Cant wait to do this again", None, "I cant drive", None, "How do you play", None, "Woop", None, ]
                    ,"Ben" : ["Crazy", None, "was not bad", None, "who else is coming", None, "anyone want to come with me", None, "look good", None, ]
                    ,"Jamie": ["Best Night ever", None, "Nice", None, "CANT WAIT", None, "I DONT LIKE CHESS", None, None, "THIS IS SO GOOD, FINALLY IT WILL BE CLEAN", ]
                   }
    
       
    #Populate Comments
    for name in UserComments:  
        for i in range(10):     
            if UserComments[name][i] != None:  
                #call add comment with user, event and comment message 
                E = Event.objects.get(title=Events["title"][i])
                U = User.objects.get(username=name)
                add_comment(E, U, UserComments[name][i])    
                
    

    
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
    
   
   
def add_comment(event, user, data):

    C = Comment.objects.get_or_create(
    event=event,
    user=user,
    data=data)


if __name__ == '__main__':  
    print("Population Eventmaker with population script...")
    populate()
        