import os

import django
from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from eventmakerapp.forms import Address
from eventmakerapp.models import Event, Like

FAILURE_HEADER = f"{os.linesep}{os.linesep}{os.linesep}================{os.linesep}Eventmaker TEST FAILURE =({os.linesep}================{os.linesep}"
FAILURE_FOOTER = f"{os.linesep}"

f"{FAILURE_HEADER} {FAILURE_FOOTER}"



class index_tests(TestCase):
    fixtures = ['eventmakerapp/fixtures/eventmakerapp_views_testdata.json', ]

    def setUp(self):

        assert Event.objects.exists()
        self.client = Client()
        self.user = User.objects.create_user('john', 'h@h.com', 'johnpassword')


#aa

    def test_popular(self):
        #tests the most liked events are presented in popular events
        request = self.client.get(reverse('eventmakerapp:index'))
        context = request.context
        self.assertQuerysetEqual(list(context['popular']), ['<Event: Hive Thursday>',
                                                        '<Event: MCFLY>',
                                                        '<Event: NICK CAVE AND THE BAD SEEDS>',
                                                        '<Event: Music Show>',
                                                        '<Event: Open Mic Night>',
                                                        '<Event: Happy Hour>',
                                                        ])

    def test_nearest(self):
        #test the pick location form is correct
        form_data = {'location': '0.0,0.0', 'entry': ''}
        form = Address(data=form_data)
        self.assertTrue(form.is_valid())

        #check that the correct events get picked as nearest
        response = self.client.post(
            reverse('eventmakerapp:checkLocation'), data={'location': '0.0,0.0', 'entry': ''}
        )
        context = response.context
        print(context['near'])


    def test_more_events(self):
        #test that more events contains the correct events
        request = self.client.get(reverse('eventmakerapp:index'))
        context = request.context


        self.assertQuerysetEqual(list(context['more']), ['<Event: Chess Tournement>',
                                                    '<Event: Highland Ceilidh>',
                                                    '<Event: Fun Run>',
                                                    '<Event: Litter Picking in Kelvingrove Park>'])

    def test_like(self):
        pass

    def testLogin(self):
        self.client.login(username='john', password='johnpassword')



