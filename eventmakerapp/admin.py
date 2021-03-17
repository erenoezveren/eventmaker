from django.contrib import admin
from eventmakerapp.models import Event, User, Comment

admin.site.register(Event)
admin.site.register(User)
admin.site.register(Comment)