from django.contrib import admin
from eventmakerapp.models import Event, UserProfile, Comment

admin.site.register(Event)
admin.site.register(UserProfile)
admin.site.register(Comment)