import os
import importlib
from django.urls import reverse
from django.test import TestCase
from django.conf import settings
# Create your tests here.
failure_heading = f"{os.linesep}{os.linesep}{os.linesep}================{os.linesep}Eventmaker Test Failure =({os.linesep}================{os.linesep}"

class EventmakerViewsUnitTests(TestCase):

	def setUp(self):
		self.views_module = importlib.import_module('eventmakerapp.views')
		self.functions_module = importlib.import_module('eventmakerapp.functions')
		self.views_module_listing = dir(self.views_module)

	def test_viewsExist(self):
		#tests to determine whether all the necessary views are present in views.py
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


		self.assertTrue(index_exists, f"{failure_heading}Eventmaker index view does not exist.")
		self.assertTrue(show_event_exists, f"{failure_heading}Eventmaker show_event view does not exist.")
		self.assertTrue(like_exists, f"{failure_heading}Eventmaker LikeView view does not exist.")
		self.assertTrue(search_exists, f"{failure_heading}Eventmaker eventsearch view does not exist.")
		self.assertTrue(comment_exists, f"{failure_heading}Eventmaker makecomment view does not exist.")
		self.assertTrue(checkLocation_exists, f"{failure_heading}Eventmaker checkLocation view does not exist.")
		self.assertTrue(register_exists, f"{failure_heading}Eventmaker register view does not exist.")
		self.assertTrue(login_exists, f"{failure_heading}Eventmaker user_login view does not exist.")
		self.assertTrue(logout_exists, f"{failure_heading}Eventmaker user_logout view does not exist.")
		self.assertTrue(userprofile_exists, f"{failure_heading}Eventmaker userProfile view does not exist.")
		self.assertTrue(addevent_exists, f"{failure_heading}Eventmaker addEvent view does not exist.")

	def test_Index(self):
		#test to check if the index_helper function is callable
		self.assertTrue(callable(self.functions_module.index_helper), f"{failure_heading}index helper function is not defined correctly")

