import os

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from eventmakerapp.models import Event, Like

FAILURE_HEADER = f"{os.linesep}{os.linesep}{os.linesep}================{os.linesep}Eventmaker TEST FAILURE =({os.linesep}================{os.linesep}"
FAILURE_FOOTER = f"{os.linesep}"

f"{FAILURE_HEADER} {FAILURE_FOOTER}"

def create_user_object():
    """
    Helper function to create a User object.
    """
    user = User.objects.get_or_create(username='testuser',
                                      first_name='Test',
                                      last_name='User',
                                      email='test@test.com')[0]
    user.set_password('testabc123')
    user.save()

    return user


def create_events():
    """
	Helper function to create Events.
    """
    event1 = Event.objects.create(title = 'event1',
                                        description = 'empty',
                                        location = '10.0,10.0',
                                        host = create_user_object(),)

    event2 = Event.objects.create(title='event2',
                                         description='empty',
                                         location='10.0,10.0',
                                         host=create_user_object(), )

    event3 = Event.objects.create(title='event3',
                                         description='empty',
                                         location='1.0,1.0',
                                         host=create_user_object(), )

    event4 = Event.objects.create(title='event4',
                                         description='empty',
                                         location='10.0,10.0',
                                         host=create_user_object(), )

    event5 = Event.objects.create(title='event5',
                                         description='empty',
                                         location='10.0,10.0',
                                         host=create_user_object(), )

    like1 = Like.objects.create(event=event3,
                                       user=create_user_object())

class index_tests(TestCase):

    def setUp(self):
        create_events()

    def test_popular(self):
        request = self.client.get(reverse('eventmakerapp:index'))
        print(request)
