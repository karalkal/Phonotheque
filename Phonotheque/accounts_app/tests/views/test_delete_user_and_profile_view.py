from datetime import date

from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.messages.storage.fallback import FallbackStorage

from Phonotheque.accounts_app.models import Profile
from Phonotheque.accounts_app.views import delete_user_and_profile


class DeleteUserAndProfileTests(TestCase):
    VALID_STAFF_DATA = {
        'username': "bigboss",
        'password': '11111111',
        'email': "admin@user.com",
        'first_name': 'Big',
        'last_name': 'Boss',
        'is_superuser': True,
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
        'description': 'some amazing description'

    }

    def setUp(self) -> None:
        self.factory = RequestFactory()

        self.admin = User.objects.create(**self.VALID_STAFF_DATA)
        self.regular_user = User.objects.create(**self.VALID_USER_DATA)

        self.admin_profile = Profile.objects.create(user=self.admin, **self.VALID_PROFILE_DATA)
        self.regular_profile = Profile.objects.create(user=self.regular_user, **self.VALID_PROFILE_DATA)

        # TESTS

    def test_delete_user_view__redirects_to_correct_template(self):
        response = self.client.post(reverse('profile-delete', kwargs={'pk': 4444}))

        self.assertTrue(response.status_code, 302)
        self.assertTemplateUsed(reverse('profiles-list'))

    def test_delete_user_view__if_logged_in_user_is_staff__should_delete_selected_user(self):
        # Create an instance of a GET request.
        request = self.factory.post(reverse('user-deactivate-reactivate', kwargs={'user_pk': self.regular_user.pk}))

        # 2 Users exist - admin and regular
        self.assertTrue(User.objects.count() == 2)

        # Use this workaround to avoid error:
        # MessageFailure: You cannot add messages without installing django.contrib.messages.middleware.MessageMiddleware

        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        # admin logs in
        request.user = self.admin

        # Test func-based view
        response = delete_user_and_profile(request, self.regular_user.pk)

        # regular user must be deleted now
        self.assertTrue(User.objects.count() == 1)

    def test_delete_user_view__if_logged_in_user_is_staff__should_delete_own_account(self):
        # Create an instance of a GET request.
        request = self.factory.post(reverse('user-deactivate-reactivate', kwargs={'user_pk': self.regular_user.pk}))

        # 2 Users exist - admin and regular
        self.assertTrue(User.objects.count() == 2)

        # Use this workaround to avoid error:
        # MessageFailure: You cannot add messages without installing django.contrib.messages.middleware.MessageMiddleware

        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        # user logs in
        request.user = self.regular_user

        # Test func-based view
        response = delete_user_and_profile(request, self.regular_user.pk)

        # regular user must have deleted their account now
        self.assertTrue(User.objects.count() == 1)