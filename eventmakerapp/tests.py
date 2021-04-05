import os
import importlib
from django.urls import reverse
from django.test import TestCase
from django.conf import settings
# Create your tests here.
FAILURE_HEADER = f"{os.linesep}{os.linesep}{os.linesep}================{os.linesep}Eventmaker Test Failure =({os.linesep}================{os.linesep}"
FAILURE_FOOTER = f"{os.linesep}"

class EventmakerUnitTests(TestCase):
	def TestingSetUp(self):
		self.views_module = importlib.import_module('eventmakerapp.views')
		self.views_module_listing = dir(self.views_module)
    
