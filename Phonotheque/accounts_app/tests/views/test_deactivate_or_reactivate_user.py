from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory
from django.urls import reverse

from Phonotheque.accounts_app.views import deactivate_or_reactivate_user


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

    VALID_USER_DATA_INACTIVE = {
        'username': "inactive_user",
        'password': '11111111',
        'email': "test@user.com",
        'first_name': 'Inactive',
        'last_name': 'User',
        'is_active': False,
    }

    def setUp(self) -> None:
        self.factory = RequestFactory()
        self.admin = User.objects.create(**self.VALID_STAFF_DATA)
        self.regular_user = User.objects.create(**self.VALID_USER_DATA)
        self.inactive_user = User.objects.create(**self.VALID_USER_DATA_INACTIVE)

        # TESTS

    def test_get_deactivate_or_reactivate_view__should_switch_user_status(self):
        admin_login_data = {'username': 'bigboss', 'password': '11111111', }

        self.assertTrue(self.regular_user.is_active)
        self.assertFalse(self.inactive_user.is_active)

        self.client.login(**admin_login_data)

        response = self.client.get(reverse('user-deactivate-reactivate', kwargs={'user_pk': self.regular_user.pk}))
        self.assertEqual(302, response.status_code)
        self.assertEqual(f'/accounts/login/?next=/accounts/disable/{self.regular_user.pk}/', response.url)

    def test__deactivate_or_reactivate_view__verify_template(self):
        # Create an instance of a GET request.
        request = self.factory.get(reverse('user-deactivate-reactivate', kwargs={'user_pk': self.regular_user.pk}))

        # You can simulate a logged-in user by setting request.user manually.
        request.user = self.admin

        # Or you can simulate an anonymous user by setting request.user to an AnonymousUser instance.
        # request.user = AnonymousUser()

        # Test func-based view
        response = deactivate_or_reactivate_user(request, self.regular_user.pk)
        # Test class-based views.
        # response = MyView.as_view()(request)
        self.assertEqual(response.status_code, 200)
