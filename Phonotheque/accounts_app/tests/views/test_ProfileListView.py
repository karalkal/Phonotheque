from datetime import date

from django.contrib import auth

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse, reverse_lazy

from Phonotheque.accounts_app.models import Profile

UserModel = auth.get_user_model()


class ProfilesListViewTests(TestCase):
    VALID_USER_DATA_1 = {
        'username': "test_user",
        'password': '11111111',
        'email': "test@user.com",
        'first_name': 'Test',
        'last_name': 'User',
    }

    VALID_USER_DATA_2 = {
        'username': "test_useralabalanica",
        'password': '11111111alabalanica',
        'email': "testalabalanica@user.com",
        'first_name': 'Testalabalanica',
        'last_name': 'Useralabalanica',
    }

    VALID_PROFILE_DATA_1 = {
        'date_of_birth': date(1988, 4, 13),
        'photo_URL': 'https://cdn.pixabay.com/photo/2017/05/11/08/48/woman-2303361_960_720.jpg',
        'gender': 'Male',
        'description': 'some amazing description'

    }

    def __create_valid_user_and_profile(self):
        new_user = User.objects.create_user(**self.VALID_USER_DATA_1)
        new_profile = Profile.objects.create(user=new_user,
                                             **self.VALID_PROFILE_DATA_1)
        return new_user, new_profile

    def __get_response_for_profile(self, profile):
        return self.client.get(reverse('profile-details', kwargs={'pk': profile.pk}))

    # TESTS

    def test_get__when_two_users__expect_context_to_contain_two_profiles(self):
        new_user = User.objects.create_user(**self.VALID_USER_DATA_1)
        # create profile
        new_profile = Profile.objects.create(user=new_user)
        # test profile
        self.assertEqual(new_profile.user_id, new_user.pk)

        self.assertEqual(len(Profile.objects.all()), 1)

        new_user_2 = User.objects.create_user(**self.VALID_USER_DATA_2)
        # create profile
        new_profile_2 = Profile.objects.create(user=new_user_2)
        # test profile
        self.assertEqual(new_profile_2.user_id, new_user_2.pk)

        self.assertEqual(len(Profile.objects.all()), 2)
