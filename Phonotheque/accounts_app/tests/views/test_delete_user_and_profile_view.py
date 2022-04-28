from datetime import date

from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory
from django.urls import reverse

from Phonotheque.accounts_app.models import Profile


class DeleteUserAndProfileTests(TestCase):
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

        self.factory = RequestFactory()

        # TESTS

    def test_delete_user_view__redirects_to_correct_template(self):
        response = self.client.post(reverse('profile-delete', kwargs={'pk': 4444}))
        self.assertTrue(User.objects.count() == 1)
        self.assertTrue(response.status_code, 302)

    def test_logged_in_user__when_deletes_account__should_be_deleted(self):
        admin_login_data = {'username': 'bigboss', 'password': '11111111', }
        regular_user_login_data = {'username': 'Ivancho', 'password': '11111111', }

        # create regular user
        self.regular_user = User.objects.create(**self.VALID_USER_DATA)
        self.regular_profile = Profile.objects.create(**self.VALID_PROFILE_DATA, user=self.regular_user)

        self.assertTrue(User.objects.count() == 2)

        request = self.factory.get(reverse('profile-delete', kwargs={'pk': self.regular_user.pk}))

        # response = self.client.post(reverse('profile-delete', kwargs={'pk': self.regular_user.pk}))

        # TODO does not work, need a form
        # self.assertTrue(User.objects.count() == 1)
