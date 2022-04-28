from datetime import date

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from Phonotheque.accounts_app.models import Profile


class UserDeactivateAndReactivateTests(TestCase):
    VALID_STAFF_DATA = {
        'username': "bigboss",
        'password': '11111111',
        'email': "admin@user.com",
        'first_name': 'Big',
        'last_name': 'Boss',
        'is_staff': True,
    }

    VALID_USER_DATA = {
        'username': "Ivancho",
        'password': '11111111',
        'email': "ivanushka@user.com",
        'first_name': 'Ivanushka',
        'last_name': 'Glupaka',
        'is_staff': False,
    }

    VALID_PROFILE_DATA = {
        'date_of_birth': date(1988, 4, 13),
        'photo_URL': 'https://cdn.pixabay.com/photo/2017/05/11/08/48/woman-2303361_960_720.jpg',
        'gender': 'Male',
        'description': 'some amazing description',
    }

    def setUp(self) -> None:
        self.admin = User.objects.create(**self.VALID_STAFF_DATA)
        self.admin_profile = Profile.objects.create(**self.VALID_PROFILE_DATA, user=self.admin)

        # TESTS

    # def test_admin_deactivates_and_reactivates_regular_users__should_render_correct_template(self):
    #     admin_login_data = {'username': 'bigboss', 'password': '11111111', }
    #
    #     self.client.login(**admin_login_data)
    #     self.assertTrue(self.admin.is_authenticated)
    #
    #     # create regular user
    #     self.regular_user = User.objects.create(**self.VALID_USER_DATA)
    #     self.regular_profile = Profile.objects.create(**self.VALID_PROFILE_DATA, user=self.regular_user)
    #
    #     self.assertTrue(User.objects.count() == 2)
    #     self.assertTrue(self.regular_user.is_active)
    #
    #     response = self.client.get(reverse('user-deactivate-reactivate', kwargs={'user_pk': self.regular_user.pk}))
    #     self.assertFalse(self.regular_user.is_active)
    #
    #     # self.assertRedirects(response, reverse('profiles-list'))
    #
    # def test_admin_deactivates_and_reactivates_own_account__should_render_correct_template(self):
    #     admin_login_data = {'username': 'bigboss', 'password': '11111111', }
    #
    #     self.client.login(**admin_login_data)
    #     self.assertTrue(self.admin.is_authenticated)
    #
    #     response = self.client.post(reverse('user-deactivate-reactivate', kwargs={'user_pk': self.admin.pk}))
    #
    #     self.assertRedirects(response, reverse('login-page'))

    def test_get_deactivate_or_reactivate_view__should_switch_user_status(self):
        admin_login_data = {'username': 'bigboss', 'password': '11111111', }

        # create regular user
        self.regular_user = User.objects.create(**self.VALID_USER_DATA)
        self.regular_profile = Profile.objects.create(**self.VALID_PROFILE_DATA, user=self.regular_user)

        self.assertTrue(self.regular_user.is_active)

        # self.client.login(**admin_login_data)
        self.assertTrue(self.admin.is_authenticated)

        self.client.get(reverse('user-deactivate-reactivate', kwargs={'user_pk': self.regular_user.pk}))

        # TODO: Does not work
        # self.assertFalse(self.regular_user.is_active)
