from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory
from django.urls import reverse

from Phonotheque.accounts_app.views import deactivate_or_reactivate_user
from django.contrib.messages.storage.fallback import FallbackStorage


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

    def setUp(self) -> None:
        self.factory = RequestFactory()
        self.admin = User.objects.create(**self.VALID_STAFF_DATA)
        self.regular_user = User.objects.create(**self.VALID_USER_DATA)

        # TESTS

    def test__deactivate_or_reactivate_view__redirects_to_correct_template(self):
        admin_login_data = {'username': 'bigboss', 'password': '11111111', }

        self.assertTrue(self.regular_user.is_active)

        self.client.login(**admin_login_data)

        response = self.client.get(reverse('user-deactivate-reactivate', kwargs={'user_pk': self.regular_user.pk}))
        self.assertEqual(302, response.status_code)
        self.assertEqual(f'/accounts/login/?next=/accounts/disable/{self.regular_user.pk}/', response.url)
        self.assertTemplateUsed(reverse('profiles-list'))

    def test_get_deactivate_or_reactivate_view__if_logged_in_user_is_staff__should_switch_user_status(self):
        # Create an instance of a GET request.
        request = self.factory.get(reverse('user-deactivate-reactivate', kwargs={'user_pk': self.regular_user.pk}))

        # User is active now
        self.assertTrue(User.objects.get(pk=self.regular_user.pk).is_active)

        # Use this workaround to avoid error:
        # MessageFailure: You cannot add messages without installing django.contrib.messages.middleware.MessageMiddleware

        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        # You can simulate a logged-in user by setting request.user manually.
        request.user = self.admin

        # Test func-based view
        response = deactivate_or_reactivate_user(request, self.regular_user.pk)

        # User state must be switched to NOT is_active now
        self.assertFalse(User.objects.get(pk=self.regular_user.pk).is_active)

        response = deactivate_or_reactivate_user(request, self.regular_user.pk)

        # User state must be switched BACK to is_active
        self.assertTrue(User.objects.get(pk=self.regular_user.pk).is_active)

    def test_get_deactivate_or_reactivate_view__if_logged_in_user_is_regular__should_switch_user_status(self):
        # Create an instance of a GET request.
        request = self.factory.get(reverse('user-deactivate-reactivate', kwargs={'user_pk': self.regular_user.pk}))

        # User is active now
        self.assertTrue(User.objects.get(pk=self.regular_user.pk).is_active)

        # Use this workaround to avoid error:
        # MessageFailure: You cannot add messages without installing django.contrib.messages.middleware.MessageMiddleware

        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        # You can simulate a logged-in user by setting request.user manually.
        request.user = self.regular_user

        # Test func-based view
        response = deactivate_or_reactivate_user(request, self.regular_user.pk)

        # User state cannot be switched to NOT is_active because logged-in user not is_staff
        self.assertTrue(User.objects.get(pk=self.regular_user.pk).is_active)

        response = deactivate_or_reactivate_user(request, self.regular_user.pk)

        # User state must been switched BACK to is_active
        self.assertTrue(User.objects.get(pk=self.regular_user.pk).is_active)
