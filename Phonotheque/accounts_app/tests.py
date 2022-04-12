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

    def test_user_and_profile_creation_with_valid_data_expect_profile_linked_to_user_to_be_created(self):
        new_user = User.objects.create_user(**self.VALID_USER_DATA)
        # test user
        self.assertEqual(new_user.username, "test_user")
        self.assertEqual(new_user.email, "test@user.com")
        self.assertIs(new_user.is_superuser, False)
        self.assertIs(new_user.is_staff, False)
        # create profile
        new_profile = Profile.objects.create(user=new_user,
                                             first_name=new_user.first_name,
                                             last_name=new_user.last_name, )
        # test profile
        self.assertEqual(new_profile.first_name, "Test")
        self.assertEqual(new_profile.last_name, "User")
        self.assertEqual(new_profile.user_id, new_user.pk)

    def test_user_creation_form__with_single_char_name__raises(self):
        invalid_first_name_data = {
            'username': "username",
            'first_name': "a",
            'last_name': "good name",
            'password': "123jgfhtehkjchj",
        }
        form = UserRegistrationForm(invalid_first_name_data)

        # form fails
        self.assertFalse(form.is_valid())
        # won't be saved
        with self.assertRaises(Exception) as context:
            form.save()
        self.assertEqual("The User could not be created because the data didn't validate.", str(context.exception))
        # display message
        self.assertIn("Ensure this value has at least 2 characters (it has 1).", form.errors['first_name'])

    def test_user_creation_form__with_prohibited_chars_name__raises(self):
        data = {
            'username': "username",
            'last_name': "good name",
            'password': "123jgfhtehkjchj",
        }

        invalid_first_names = ['123456', 'Ivan~', 'Pes#o', '@@', '\/+-', '==', '$%£', '\"\"']

        for invalid_f_name in invalid_first_names:
            data['first_name'] = invalid_f_name
            form = UserRegistrationForm(data)

            # form fails
            self.assertFalse(form.is_valid())
            # won't be saved
            with self.assertRaises(Exception) as context:
                form.save()
            self.assertEqual("The User could not be created because the data didn't validate.", str(context.exception))
            # display message
            self.assertIn("This name format won't work here, buddy.", form.errors['first_name'])


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
        new_profile = Profile.objects.create(user=new_user,
                                             first_name=new_user.first_name,
                                             last_name=new_user.last_name,
                                             **self.VALID_PROFILE_DATA)
        return new_user, new_profile

    def test_when_editing_user_data__expect_updated_values(self):
        user, profile = self.__create_valid_user_and_profile()
        user.first_name = "New name"
        profile.first_name = user.first_name
        self.assertEqual("New name", profile.first_name)


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
        return self.client.get(reverse('profile_details', kwargs={'pk': profile.pk}))

    # TESTS

    def test_when_opening_non_existing_profile__expect_404(self):
        response = self.client.get(reverse('profile_details', kwargs={'pk': 1}))
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
