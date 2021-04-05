from django.contrib import admin
from eventmakerapp.models import Event, UserProfile, Comment, Like

#models for admin view
admin.site.register(Event)
admin.site.register(UserProfile)
admin.site.register(Comment)
admin.site.register(Like)