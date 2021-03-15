from django.contrib import admin
from eventmakerapp.models import Event, User, BusinessProfile, Comment, UserProfile

admin.site.register(Event)
admin.site.register(User)
admin.site.register(BusinessProfile)
admin.site.register(Comment)
admin.site.register(UserProfile)