from django.contrib import admin
from eventmakerapp.models import Event, User, Business, Comment, Account

admin.site.register(Event)
admin.site.register(User)
admin.site.register(Business)
admin.site.register(Comment)
admin.site.register(Account)