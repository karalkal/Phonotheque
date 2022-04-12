from datetime import date

from django import test as django_test
from django.contrib.auth import get_user_model
from django.urls import reverse

from Phonotheque.accounts_app.models import Profile

User = get_user_model()


class UserAndProfileCreationTests(django_test.TestCase):
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

    def test_user_and_profile_creation_with_valid_data_expect_profile_linked_to_user(self):
        new_user = User.objects.create_user(**self.VALID_USER_DATA)

        self.assertEqual(new_user.username, "test_user")
        self.assertEqual(new_user.email, "test@user.com")
        self.assertIs(new_user.is_superuser, False)
        self.assertIs(new_user.is_staff, False)

        new_profile = Profile.objects.create(user=new_user,
                                             first_name=new_user.first_name,
                                             last_name=new_user.last_name, )

        self.assertEqual(new_profile.first_name, "Test")
        self.assertEqual(new_profile.last_name, "User")
        self.assertEqual(new_profile.user_id, new_user.pk)


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

    def test_when_opening_not_existing_profile__expect_404(self):
        response = self.client.get(reverse('profile_details', kwargs={'pk': 1}))
        self.assertEqual(404, response.status_code)

    def test_when_opening_existing_profile__expect_correct_template(self):
        _, profile = self.__create_valid_user_and_profile()
        self.__get_response_for_profile(profile)
        self.assertTemplateUsed('accounts_app/profile_details.html')
