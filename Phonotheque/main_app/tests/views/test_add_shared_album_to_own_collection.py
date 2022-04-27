from datetime import datetime

from django import test as django_test
from django.contrib.auth import get_user_model
from django.urls import reverse

from Phonotheque.main_app.models import Collection, Album, Artist

User = get_user_model()


class ArtistAndAlbumDataSaveTests(django_test.TestCase):
    VALID_ARTIST = {
        'id': 88,
        'name': 'Meshuggah',
    }

    VALID_ALBUM = {
        'wiki_id': 11111111,
        'title': 'Album1',
        'wiki_url': 'https://en.album1.org',
        'summary': 'studio album 1',
        'resume': 'Nothing1',
        'album_cover': 'https://upload.wikimedia.org/cover.jpg',
        'time_created': datetime.now(),
        'artist_id': 88,
    }

    VALID_USER_DATA = {
        'username': "test_user",
        'password': '11111111',
        'email': "test@user.com",
        'first_name': 'Test',
        'last_name': 'User',
    }

    VALID_USER_DATA_2 = {
        'username': "test_user_ZWEI",
        'password': '11111111',
        'email': "test@user.com",
        'first_name': 'Number',
        'last_name': 'Two',
    }

    VALID_COLLECTION_ITEM = {'album_id': '11111111',
                             'time_created': datetime.now()
                             }

    # TESTS

    def setUp(self) -> None:
        self.artist = Artist.objects.create(**self.VALID_ARTIST)
        self.album = Album.objects.create(**self.VALID_ALBUM)
        self.user = User.objects.create_user(**self.VALID_USER_DATA)
        self.user_2 = User.objects.create_user(**self.VALID_USER_DATA_2)

    def test_get__expect_to_redirect_to_correct_template(self):
        Collection.objects.create(user=self.user, album=self.album)
        user_data = {'username': 'test_user_ZWEI', 'password': '11111111', }
        self.client.login(**user_data)

        response = self.client.get(reverse('save_shared_album', kwargs={'album_wiki_id': 11111111}))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('dashboard'))

    def test_album__when_album_exists_and_another_users_adds_to_their_collection__both_must_have_it(self):
        Collection.objects.create(user=self.user, album=self.album)
        # user2 does not have it in their collection
        user_data = {'username': 'test_user_ZWEI', 'password': '11111111', }

        self.client.login(**user_data)

        # just verification, real tests will be below
        response = self.client.get(reverse('album_details', kwargs={'pk': 11111111}))
        self.assertEqual(1, len(response.context_data['others_who_liked_it']))
        self.assertFalse(response.context_data['liked_by_current_user'])
        user_1_collection = Album.objects.filter(collection__user_id=self.user.pk)
        user_2_collection = Album.objects.filter(collection__user_id=self.user_2.pk)

        Collection.objects.create(user=self.user_2, album=self.album)

        self.assertQuerysetEqual(user_1_collection, user_2_collection)
