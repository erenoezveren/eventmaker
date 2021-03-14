import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'eventmaker.settings')

import django
django.setup()
from eventmakerapp.models import Business, User, Event, Comment

def populate():

    pass