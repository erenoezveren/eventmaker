from django.contrib import admin
from eventmakerapp.models import Event, User, Business, Comment

admin.site.register(Event)
admin.site.register(User)
admin.site.register(Business)
admin.site.register(Comment)