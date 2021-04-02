from django.contrib import admin
from eventmakerapp.models import Event, UserProfile, Comment, Join, Like

admin.site.register(Event)
admin.site.register(UserProfile)
admin.site.register(Comment)
admin.site.register(Join)
admin.site.register(Like)