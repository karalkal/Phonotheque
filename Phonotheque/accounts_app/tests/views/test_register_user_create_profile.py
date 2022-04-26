from datetime import date

from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory
from django.urls import reverse

from Phonotheque.accounts_app.forms import UserRegistrationForm
from Phonotheque.accounts_app.models import Profile


class ProfileCreateViewTests(TestCase):
    VALID_USER_DATA = {
        'username': "test_user",
        'password': '11111111',
        'email': "test@user.com",
        'first_name': 'Test',
        'last_name': 'User',
    }

    VALID_PROFILE_DATA = {
        'date_of_birth': date(1988, 4, 13),
        'photo_URL': 'https://cdn.pixabay.com/photo/2017/05/11/08/48/woman-2303361_960_720.jpg',
        'gender': 'Male',
        'description': 'some amazing description'
    }

    def test_get_register_view__should_render_correct_template(self):
        response = self.client.get('')
        self.assertTemplateUsed(response, 'main_app/index.html')

    def test_user_and_profile_creation__with_valid_data__expect_both_to_be_created(self):
        new_user = User.objects.create_user(**self.VALID_USER_DATA)
        # test user
        self.assertEqual(new_user.username, "test_user")
        self.assertEqual(new_user.email, "test@user.com")
        self.assertIs(new_user.is_superuser, False)
        self.assertIs(new_user.is_staff, False)
        # create profile
        new_profile = Profile.objects.create(user=new_user)
        # test profile
        self.assertEqual(new_profile.user_id, new_user.pk)
        # test correct url
        self.assertTemplateUsed('/accounts/register/')

    def test_create_user__with_one_char_first_name__raises(self):
        INVALID_FIRST_NAME_DATA = {
            'username': "username",
            'email': "baba@baba.com",
            'first_name': "A",
            'last_name': "good Lastname",
            'password': "123jgfhtehkjchj!!!!!!JHAJHSJHJHS",
            'password2': "123jgfhtehkjchj!!!!!!JHAJHSJHJHS",
        }

        user_form = UserRegistrationForm(INVALID_FIRST_NAME_DATA)
        try:
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
        except ValueError as ex:
            self.assertIsNotNone(ex)
            self.assertEqual("The User could not be created because the data didn't validate.", str(ex))
