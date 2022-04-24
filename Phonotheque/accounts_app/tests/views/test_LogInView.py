from django import test as django_test
from django.contrib.auth import get_user_model

User = get_user_model()


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
