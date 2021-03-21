from django.urls import path 
from eventmakerapp import views

app_name = 'eventmakerapp'

urlpatterns = [
    path('', views.index, name='index'),  
    path('about/', views.about, name="about"),
    path('event/<event_name>', views.show_event, name='show_event'),
    path('eventsearch/', views.eventsearch, name='eventsearch'),
    path('event/<event_name>/makecomment', views.makecomment, name='makecomment'),
    #path('user/<user_name>/', views.user, name='user')
    path('user/<user_name>/pickLocation/', views.pickLocation, name='pickLocation')
]
