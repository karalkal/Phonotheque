from datetime import date

from django import test as django_test
from django.contrib.auth import get_user_model
from django.urls import reverse

from Phonotheque.accounts_app.forms import UserRegistrationForm
from Phonotheque.accounts_app.models import Profile

User = get_user_model()


class UserAndProfileCreateTests(django_test.TestCase):
    VALID_USER_DATA = {
        'username': "test_user",
        'password': '11111111',
        'email': "test@user.com",
        'first_name': 'Test',
        'last_name': 'User',
    }

    VALID_PROFILE_DATA = {
        'date_of_birth': date(1988, 4, 13),
        'photo_url': 'https://cdn.pixabay.com/photo/2017/05/11/08/48/woman-2303361_960_720.jpg',
        'gender': 'Male',
        'description': 'some amazing description'

    }

    def test_user_and_profile_creation__with_valid_data__expect_profile_to_be_created(self):
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


class UserAndProfileEditTests(django_test.TestCase):
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

    def __create_valid_user_and_profile(self):
        new_user = User.objects.create_user(**self.VALID_USER_DATA)
        new_profile = Profile.objects.create(
            user=new_user,
            **self.VALID_PROFILE_DATA
        )
        return new_user, new_profile

    def test_when_editing_user_data__expect_updated_values(self):
        user, profile = self.__create_valid_user_and_profile()
        user.first_name = "New name"
        self.assertEqual("New name", user.first_name)


class ProfileDetailsViewTests(django_test.TestCase):
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

    def __create_valid_user_and_profile(self):
        new_user = User.objects.create_user(**self.VALID_USER_DATA)
        new_profile = Profile.objects.create(user=new_user,
                                             first_name=new_user.first_name,
                                             last_name=new_user.last_name,
                                             **self.VALID_PROFILE_DATA)
        return new_user, new_profile

    def __get_response_for_profile(self, profile):
        return self.client.get(reverse('profile-details', kwargs={'pk': profile.pk}))

    # TESTS

    def test_when_opening_non_existing_profile__expect_404(self):
        response = self.client.get(reverse('profile-details', kwargs={'pk': 1}))
        self.assertEqual(404, response.status_code)

    def test_when_opening_existing_profile__expect_correct_template(self):
        _, profile = self.__create_valid_user_and_profile()
        self.__get_response_for_profile(profile)
        self.assertTemplateUsed('accounts_app/profile_details.html')


class LogInViewTests(django_test.TestCase):
    VALID_USER_DATA = {
        'username': "test_user",
        'password': '11111111',
        'email': "test@user.com",
        'first_name': 'Test',
        'last_name': 'User',
    }

    def test_when_user_enters__valid_credentials__user_must_log_in_successfully_and_view_dashboard(self):
        User.objects.create_user(**self.VALID_USER_DATA)
        credentials = {
            'username': 'test_user',
            'password': '11111111'}
        response = self.client.post('/accounts/login/', credentials, follow=True)
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertRedirects(response, '/dashboard/')
        self.assertEqual(response.status_code, 200)

    def test_when_user_enters__invalid_credentials__user_cannot_log(self):
        User.objects.create_user(**self.VALID_USER_DATA)
        credentials = {
            'username': 'test_user',
            'password': 'wrong_pw'}
        response = self.client.post('/accounts/login/', credentials, follow=True)
        self.assertFalse(response.context['user'].is_authenticated)

    def test_when_user_logs_out__user_must_log_out_and_redirected_to_index(self):
        User.objects.create_user(**self.VALID_USER_DATA)
        credentials = {
            'username': 'test_user',
            'password': '11111111'}
        response1 = self.client.post('/accounts/login/', credentials, follow=True)
        self.assertTrue(response1.context['user'].is_authenticated)

        response2 = self.client.post('/accounts/logout/', credentials, follow=True)
        self.assertFalse(response2.context['user'].is_authenticated)
        self.assertRedirects(response2, '/')  # index page
