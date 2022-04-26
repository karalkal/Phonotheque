from datetime import date

from django.contrib import auth

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from django.urls import reverse, reverse_lazy

from Phonotheque.accounts_app.models import Profile

User = auth.get_user_model()


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

    # TESTS

    def test_get__when_two_users__expect_context_to_contain_two_profiles(self):
        new_user = User.objects.create_user(**self.VALID_USER_DATA_1)
        new_profile = Profile.objects.create(user=new_user)

        self.assertEqual(new_profile.user_id, new_user.pk)
        self.assertEqual(len(Profile.objects.all()), 1)

        new_user_2 = User.objects.create_user(**self.VALID_USER_DATA_2)
        new_profile_2 = Profile.objects.create(user=new_user_2)

        self.assertEqual(new_profile_2.user_id, new_user_2.pk)
        self.assertEqual(len(Profile.objects.all()), 2)

    def test_view_get_context_data__with__logged_in_user_should_return_correct_context(self):
        user_data = {'username': 'BayHuy', 'password': '11111111', }
        new_user = User.objects.create_user(**user_data)

        new_profile = Profile.objects.create(user=new_user)

        self.assertEqual(len(User.objects.all()), 1)
        self.assertEqual(new_profile.user_id, new_user.pk)
        self.assertEqual(len(Profile.objects.all()), 1)

        self.client.login(**user_data)

        response = self.client.get(reverse('profiles-list'))

        self.assertEqual(
            user_data['username'],
            response.context_data['current_profile'].user.username, )

        self.assertEqual(
            new_profile, response.context_data['current_profile'])

        self.assertEqual(len(response.context_data['profile_list']), 1)

    # to test the specific scenario when Profile is not automatically created upon User creation,
    # i.e. when created by createsuperuser
    def test_view_get_context_data__with__logged_in_superuser_should_create_profile_return_correct_context(self):
        user_data = {'username': 'BayHuy', 'password': '11111111', }
        new_user = User.objects.create_user(**user_data)

        self.client.login(**user_data)

        response = self.client.get(reverse('profiles-list'))
        print(Profile.objects.get(pk=new_user.pk))
        try:
            new_profile = Profile.objects.get(pk=new_user.pk)
            a = 5
        except ObjectDoesNotExist:
            new_profile = Profile.objects.create(user=new_user)
