from django.urls import path 
from eventmakerapp import views

app_name = 'eventmakerapp'

urlpatterns = [
    path('', views.index, name='index'),  
    path('about/', views.about, name="about"),
    path('event/<event_name>', views.show_event, name='show_event'),
    path('eventsearch/', views.eventsearch, name='eventsearch'),
    path('event/<event_name>/makecomment', views.makecomment, name='makecomment'),
    path('user/<user_name>/', views.userProfile, name='userProfile'),
    path('checkLocation', views.checkLocation, name='checkLocation'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('like/', views.like_event, name='like_event'),
    path('join/', views.join_event, name = 'join_event'),
    path('addEvent/', views.addEvent, name='addEvent'),
    ]