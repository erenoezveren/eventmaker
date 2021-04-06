import os

import django
from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from eventmakerapp.forms import Address, EventForm
from eventmakerapp.models import Event, Like

failure_heading = f"{os.linesep}{os.linesep}{os.linesep}================{os.linesep}Eventmaker TEST FAILURE =({os.linesep}================{os.linesep}"
FAILURE_FOOTER = f"{os.linesep}"

f"{failure_heading} {FAILURE_FOOTER}"



class function_tests(TestCase):
    fixtures = ['eventmakerapp/fixtures/eventmakerapp_views_testdata.json', ]

    def setUp(self):

        assert Event.objects.exists()
        self.client = Client()
        self.user = User.objects.create_user('john', 'h@h.com', 'johnpassword')


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
        self.assertQuerysetEqual(list(context['near']), ['<Event: Fun Run>',
                                                        '<Event: MCFLY>',
                                                        '<Event: NICK CAVE AND THE BAD SEEDS>',
                                                        '<Event: Music Show>',
                                                        '<Event: Litter Picking in Kelvingrove Park>',
                                                        '<Event: Highland Ceilidh>',
                                                        ])


    def test_more_events(self):
        #test that more events contains the correct events
        request = self.client.get(reverse('eventmakerapp:index'))
        context = request.context


        self.assertQuerysetEqual(list(context['more']), ['<Event: Chess Tournement>',
                                                    '<Event: Highland Ceilidh>',
                                                    '<Event: Fun Run>',
                                                    '<Event: Litter Picking in Kelvingrove Park>'])

    def test_like(self):
        self.client.login(username='Bill', password='passBill')

        #check Likes on Fun Run
        likes_before = Event.objects.get(title='Highland Ceilidh').total_likes()

        #give like via LikeView
        response = self.client.post(reverse('eventmakerapp:LikeView',
                                    kwargs = {'pk':Event.objects.get(title='Highland Ceilidh').id}),
                                   {'event_id': Event.objects.get(title='Highland Ceilidh').id})

        #check Likes again
        likes_after = Event.objects.get(title='Highland Ceilidh').total_likes()

        #If test worked, likes will have increased by 1.
        self.assertEqual(1, likes_after - likes_before)

    def test_addEvent(self):
        self.client.login(username='Bill', password='passBill')

        #Check events before adding
        self.assertQuerysetEqual(list(Event.objects.all()), ['<Event: Hive Thursday>', '<Event: MCFLY>', '<Event: NICK CAVE AND THE BAD SEEDS>', '<Event: Music Show>', '<Event: Open Mic Night>', '<Event: Happy Hour>', '<Event: Chess Tournement>', '<Event: Highland Ceilidh>', '<Event: Fun Run>', '<Event: Litter Picking in Kelvingrove Park>'])

        #add using addEvent
        response = self.client.post(
            reverse('eventmakerapp:addEvent'), data={'title': 'HipHop Rap',
                                                     'description': 'Hippity Hoppity Rappity',
                                                     'locationName': 'ground',
                                                     'location': '0.0,0.0',
                                                     'entry': '',
                                                     'time': '28/04/2021 23:00',
                                                     'price': '1.0'}
        )

        #Check that events includes HipHop Rap now
        self.assertQuerysetEqual(list(Event.objects.all()), ['<Event: Hive Thursday>', '<Event: MCFLY>', '<Event: NICK CAVE AND THE BAD SEEDS>', '<Event: Music Show>', '<Event: Open Mic Night>', '<Event: Happy Hour>', '<Event: Chess Tournement>', '<Event: Highland Ceilidh>', '<Event: Fun Run>', '<Event: Litter Picking in Kelvingrove Park>',
                                                             '<Event: HipHop Rap>'])


    def test_search(self):
        #Search for 'MC'
        request = self.client.get(reverse('eventmakerapp:eventsearch'), {'searchEvent':'MC'})

        resultEvent = request.context['searches']

        #Check that the result of the search is the 'MCFLY' event
        self.assertQuerysetEqual(resultEvent, ['<Event: MCFLY>'])


