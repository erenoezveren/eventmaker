from registration.backends.default.views import RegistrationView
from eventmakerapp.forms import UserProfileRegistrationForm
from eventmakerapp.models import UserProfile

class MyRegistrationView(RegistrationView):

    form_class = UserProfileRegistrationForm

    def register(self, request, form_class):
        new_user = super(MyRegistrationView, self).register(request, form_class)

        first_name = form_class.cleaned_data['first_name']
        last_name = form_class.cleaned_data['last_name']
        is_business = form_class.cleaned_data['is_business']
        description = form_class.cleaned_data['description']
        picture = form_class.cleaned_data['picture']
        website = form_class.cleaned_data['website']

        new_profile = Profile.objects.create(user=new_user, 
        first_name = first_name,
        last_name = last_name,
        is_business = is_business,
        description = description,
        picture = picture,
        website = website)

        new_profile.save()

        return new_user
