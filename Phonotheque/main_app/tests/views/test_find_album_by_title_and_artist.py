from django import test as django_test
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


class ArtistAndAlbumDataSaveTests(django_test.TestCase):
    VALID_USER_DATA = {
        'username': "test_user",
        'password': '11111111',
        'email': "test@user.com",
        'first_name': 'Test',
        'last_name': 'User',
    }

    # TESTS

    def setUp(self) -> None:
        self.user = User.objects.create_user(**self.VALID_USER_DATA)

    def test_get__expect_to_redirect_to_correct_template(self):
        user_data = {'username': 'test_user', 'password': '11111111', }
        self.client.login(**user_data)

        response = self.client.get(reverse('find_album_by_title_and_artist'))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('dashboard'))
