import os
import importlib
from django.urls import reverse
from django.test import TestCase
from django.conf import settings
# Create your tests here.
failure_heading = f"{os.linesep}{os.linesep}{os.linesep}================{os.linesep}Eventmaker Test Failure =({os.linesep}================{os.linesep}"

class EventmakerUnitTests(TestCase):

	def setUp(self):
		self.views_module = importlib.import_module('eventmakerapp.views')
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

    def test_popular(self):

    def test_userprofile_class(self):
        """
        Does the UserProfile class exist in eventmakerapp.models? If so, are all the required attributes present?
        """
        self.assertTrue('UserProfile' in dir(eventmakerapp.models))

        user_profile = eventmakerapp.models.UserProfile()

        # Now check that all the required attributes are present.
        # We do this by building up a UserProfile instance, and saving it.
        expected_attributes = {
            'first_name': 'Test',
            'last_name': 'User',
            'is_business': True,
            'description': 'this is me',
            'picture': 'party.jpg',
            'user': create_user_object(),
        }

        expected_types = {
            'first_name': models.fields.CharField,
            'last_name': models.fields.CharField,
            'is_business': models.fields.BooleanField,
            'description': models.fields.TextField,
            'picture': models.fields.files.ImageField,
            'user': models.fields.related.OneToOneField,
        }

        found_count = 0

        for attr in user_profile._meta.fields:
            attr_name = attr.name

            for expected_attr_name in expected_attributes.keys():
                if expected_attr_name == attr_name:
                    found_count += 1

                    self.assertEqual(type(attr), expected_types[attr_name],
                                     f"{failure_heading}The type of attribute for '{attr_name}' was '{type(attr)}'; we expected '{expected_types[attr_name]}'. Please check your database. {failure_footing}")
                    setattr(user_profile, attr_name, expected_attributes[attr_name])

        self.assertEqual(found_count, len(expected_attributes.keys()),
                         f"{failure_heading}In the UserProfile model, we found {found_count} attributes, but were expecting {len(expected_attributes.keys())}. Please check your database.{failure_footing}")
        user_profile.save()

    def test_user_form(self):
            """
            Tests whether UserForm is in the correct place, and whether the correct fields have been specified for it.
            """
            self.assertTrue('UserForm' in dir(forms),
                            f"{failure_heading}We couldn't find the UserForm class in Eventmaker's forms.py module.{failure_footing}")

            user_form = forms.UserForm()
            self.assertEqual(type(user_form.__dict__['instance']), User,
                             f"{failure_heading}The UserForm does not match up to the User model. {failure_footing}")

            fields = user_form.fields

            expected_fields = {
                'username': django_fields.CharField,
                'email': django_fields.EmailField,
                'password': django_fields.CharField,
            }

            for expected_field_name in expected_fields:
                expected_field = expected_fields[expected_field_name]

                self.assertTrue(expected_field_name in fields.keys(),
                                f"{failure_heading}The field {expected_field_name} was not found in the UserForm form. Check you have complied with the specification, and try again.{failure_footing}")
                self.assertEqual(expected_field, type(fields[expected_field_name]),
                                 f"{failure_heading}The field {expected_field_name} in UserForm was not of the correct type. Expected {expected_field}; got {type(fields[expected_field_name])}.{failure_footing}")

    def test_user_profile_form(self):
            """
            Tests whether UserProfileForm is in the correct place, and whether the correct fields have been specified for it.
            """
            self.assertTrue('UserProfileForm' in dir(forms),
                            f"{failure_heading}Could not find UserProfileForm{failure_footing}")

            user_profile_form = forms.UserProfileForm()
            self.assertEqual(type(user_profile_form.__dict__['instance']), eventmakerapp.models.UserProfile,
                             f"{failure_heading}UserProfileForm does not line up with UserProfile model{failure_footing}")

            fields = user_profile_form.fields

            expected_fields = {
                'first_name': django_fields.CharField,
                'last_name': django_fields.CharField,
                'is_business': django_fields.BooleanField,
                'description': django_fields.CharField,
                'picture': django_fields.ImageField,
            }

            for expected_field_name in expected_fields:
                expected_field = expected_fields[expected_field_name]

                self.assertTrue(expected_field_name in fields.keys(),
                                f"{failure_heading}The field {expected_field_name} was not found in the UserProfile form. Check you have complied with the specification, and try again.{failure_footing}")
                self.assertEqual(expected_field, type(fields[expected_field_name]),
                                 f"{failure_heading}The field {expected_field_name} in UserProfileForm was not of the correct type. Expected {expected_field}; got {type(fields[expected_field_name])}.{failure_footing}")

    def test_login_function(self):

        user_object = create_user_object()
        response = self.client.post(reverse('eventmakerapp:login'), {'username': 'testuser', 'password': 'testabc123'})

        try:
            self.assertEqual(user_object.id, int(self.client.session['_auth_user_id']),
                f"{failure_heading}Attempted to log a user in with an ID of {user_object.id}, but instead logged in with a user of ID {self.client.session['_auth_user_id']}.{failure_footing}")
        except KeyError:
            self.assertTrue(False,
                f"{failure_heading}When attempting to log in with your login() view, it didn't seem to log the user in. Please check your login() view implementation, and try again.{failure_footing}")

        self.assertEqual(response.status_code, 302,
                         f"{failure_heading}When attempting to log in with your login() view, it didn't seem to log the user in. Please check your login() view implementation, and try again.{failure_footing}")
        self.assertEqual(response.url, reverse('eventmakerapp:index'),
                         f"{failure_heading}We were not redirected to the Rango homepage after logging in. Please check your login() view implementation, and try again.{failure_footing}")


    def test_Index(self):
        # test to check if the index_helper function is callable
        self.assertTrue(callable(self.functions_module.index_helper),
                        f"{failure_heading}index helper function is not defined correctly")


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
    event1 = Event.objects.get_or_create(title = 'event1',
                                        description = 'empty',

    ##still working here
    )
    )
