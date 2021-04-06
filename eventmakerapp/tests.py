import os
import importlib
from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from eventmakerapp.forms import Address
from eventmakerapp.models import Event

failure_heading = f"{os.linesep}{os.linesep}{os.linesep}================{os.linesep}Eventmaker TEST FAILURE =({os.linesep}================{os.linesep}"
failure_footing = f"{os.linesep}"

f"{failure_heading} {failure_footing}"


class FunctionalityTests(TestCase):
    fixtures = ['eventmakerapp/fixtures/eventmakerapp_views_testdata.json', ]

    def setUp(self):
        assert Event.objects.exists()
        self.client = Client()
        self.user = User.objects.create_user('john', 'h@h.com', 'johnpassword')

    def test_popular(self):
        # tests the most liked events are presented in popular events
        request = self.client.get(reverse('eventmakerapp:index'))
        context = request.context
        self.assertQuerysetEqual(list(context['popular']), ['<Event: Hive Thursday>',
                                                            '<Event: MCFLY>',
                                                            '<Event: NICK CAVE AND THE BAD SEEDS>',
                                                            '<Event: Music Show>',
                                                            '<Event: Open Mic Night>',
                                                            '<Event: Happy Hour>',
                                                            ],
                                 msg=f"{failure_heading}Popular Event function does not work properly!{failure_footing}")

    def test_nearest(self):
        # test the pick location form is correct
        form_data = {'location': '0.0,0.0', 'entry': ''}
        form = Address(data=form_data)
        self.assertTrue(form.is_valid(), msg=f"{failure_heading}Address form does not work properly!{failure_footing}")

        # check that the correct events get picked as nearest
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
                                                         ],
                                 msg=f"{failure_heading}Nearest Event function does not work properly!{failure_footing}")

    def test_more_events(self):
        # test that more events contains the correct events
        request = self.client.get(reverse('eventmakerapp:index'))
        context = request.context

        self.assertQuerysetEqual(list(context['more']), ['<Event: Chess Tournement>',
                                                         '<Event: Highland Ceilidh>',
                                                         '<Event: Fun Run>',
                                                         '<Event: Litter Picking in Kelvingrove Park>'],
                                 msg=f"{failure_heading}More Event function does not work properly!{failure_footing}")

    def test_like(self):
        self.client.login(username='Bill', password='passBill')

        # check Likes on Fun Run
        likes_before = Event.objects.get(title='Highland Ceilidh').total_likes()

        # give like via LikeView
        response = self.client.post(reverse('eventmakerapp:LikeView',
                                            kwargs={'pk': Event.objects.get(title='Highland Ceilidh').id}),
                                    {'event_id': Event.objects.get(title='Highland Ceilidh').id})

        # check Likes again
        likes_after = Event.objects.get(title='Highland Ceilidh').total_likes()

        # If test worked, likes will have increased by 1.
        self.assertEqual(1, likes_after - likes_before,
                         msg=f"{failure_heading}Like function does not increase likes!{failure_footing}")

    def test_addEvent(self):
        self.client.login(username='Bill', password='passBill')

        # Check events before adding
        self.assertQuerysetEqual(list(Event.objects.all()),
                                 ['<Event: Hive Thursday>', '<Event: MCFLY>', '<Event: NICK CAVE AND THE BAD SEEDS>',
                                  '<Event: Music Show>', '<Event: Open Mic Night>', '<Event: Happy Hour>',
                                  '<Event: Chess Tournement>',
                                  '<Event: Highland Ceilidh>', '<Event: Fun Run>',
                                  '<Event: Litter Picking in Kelvingrove Park>'],
                                 msg=f"{failure_heading}Events are not saved correctly!{failure_footing}")

        # add using addEvent
        response = self.client.post(
            reverse('eventmakerapp:addEvent'), data={'title': 'HipHop Rap',
                                                     'description': 'Hippity Hoppity Rappity',
                                                     'locationName': 'ground',
                                                     'location': '0.0,0.0',
                                                     'entry': '',
                                                     'time': '28/04/2021 23:00',
                                                     'price': '1.0'}
        )

        # Check that events includes HipHop Rap now
        self.assertQuerysetEqual(list(Event.objects.all()),
                                 ['<Event: Hive Thursday>', '<Event: MCFLY>', '<Event: NICK CAVE AND THE BAD SEEDS>',
                                  '<Event: Music Show>', '<Event: Open Mic Night>', '<Event: Happy Hour>',
                                  '<Event: Chess Tournement>', '<Event: Highland Ceilidh>', '<Event: Fun Run>',
                                  '<Event: Litter Picking in Kelvingrove Park>',
                                  '<Event: HipHop Rap>'],
                                 msg=f"{failure_heading}AddEvent function does not work properly!{failure_footing}")

    def test_search(self):
        # Search for 'MC'
        request = self.client.get(reverse('eventmakerapp:eventsearch'), {'searchEvent': 'MC'})

        resultEvent = request.context['searches']

        # Check that the result of the search is the 'MCFLY' event
        self.assertQuerysetEqual(resultEvent, ['<Event: MCFLY>'],
                                 msg=f"{failure_heading}Search Event function does not work properly!{failure_footing}")


class StructuralTests(TestCase):

    def setUp(self):
        self.views_module = importlib.import_module('eventmakerapp.views')
        self.views_module_listing = dir(self.views_module)

        self.functions_module = importlib.import_module('eventmakerapp.functions')
        self.functions_module_listing = dir(self.functions_module)
        self.forms_module = importlib.import_module('eventmakerapp.forms')
        self.forms_module_listing = dir(self.forms_module)
        self.urls_module = importlib.import_module('eventmakerapp.urls')
        self.urls_module_listing = dir(self.urls_module)

    def test_viewsExist(self):
        # tests to determine whether all the necessary views are present in views.py
        index_exists = 'index' in self.views_module_listing
        about_exists = 'about' in self.views_module_listing
        show_event_exists = 'show_event' in self.views_module_listing
        like_exists = 'LikeView' in self.views_module_listing
        search_exists = 'eventsearch' in self.views_module_listing
        comment_exists = 'makecomment' in self.views_module_listing
        checkLocation_exists = 'checkLocation' in self.views_module_listing
        register_exists = 'register' in self.views_module_listing
        login_exists = 'user_login' in self.views_module_listing
        logout_exists = 'user_logout' in self.views_module_listing
        userprofile_exists = 'userProfile' in self.views_module_listing
        addevent_exists = 'addEvent' in self.views_module_listing

        self.assertTrue(index_exists, f"{failure_heading}Eventmaker index view does not exist.{failure_footing}")
        self.assertTrue(show_event_exists, f"{failure_heading}Eventmaker show_event view does not exist.{failure_footing}")
        self.assertTrue(like_exists, f"{failure_heading}Eventmaker LikeView view does not exist.{failure_footing}")
        self.assertTrue(search_exists, f"{failure_heading}Eventmaker eventsearch view does not exist.{failure_footing}")
        self.assertTrue(comment_exists, f"{failure_heading}Eventmaker makecomment view does not exist.{failure_footing}")
        self.assertTrue(checkLocation_exists, f"{failure_heading}Eventmaker checkLocation view does not exist.{failure_footing}")
        self.assertTrue(register_exists, f"{failure_heading}Eventmaker register view does not exist.{failure_footing}")
        self.assertTrue(login_exists, f"{failure_heading}Eventmaker user_login view does not exist.{failure_footing}")
        self.assertTrue(logout_exists, f"{failure_heading}Eventmaker user_logout view does not exist.{failure_footing}")
        self.assertTrue(userprofile_exists, f"{failure_heading}Eventmaker userProfile view does not exist.{failure_footing}")
        self.assertTrue(addevent_exists, f"{failure_heading}Eventmaker addEvent view does not exist.{failure_footing}")

    def test_Index(self):
        # test to check if the index_helper function is callable
        self.assertTrue(callable(self.functions_module.index_helper),
                        f"{failure_heading}index helper function is not defined correctly{failure_footing}")