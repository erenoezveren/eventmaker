import os

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from eventmakerapp.models import Event, Like

FAILURE_HEADER = f"{os.linesep}{os.linesep}{os.linesep}================{os.linesep}Eventmaker TEST FAILURE =({os.linesep}================{os.linesep}"
FAILURE_FOOTER = f"{os.linesep}"

f"{FAILURE_HEADER} {FAILURE_FOOTER}"


class index_tests(TestCase):

    def setUp(self):
        fixtures = ['eventmakerapp_views_testdata.json']



    def test_popular(self):
        #tests the most liked events are presented in popular events
        request = self.client.get(reverse('eventmakerapp:index'))
        context = request.context
        print(context)



