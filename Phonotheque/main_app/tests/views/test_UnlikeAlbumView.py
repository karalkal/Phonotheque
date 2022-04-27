from datetime import datetime

from django import test as django_test
from django.contrib.auth import get_user_model

from Phonotheque.main_app.models import Collection, Album, Artist

User = get_user_model()


class UnlikeAlbumViewTests(django_test.TestCase):
    VALID_USER_DATA = {
        'username': "test_user",
        'password': '11111111',
        'email': "test@user.com",
        'first_name': 'Test',
        'last_name': 'User',
    }

    VALID_COLLECTION_ITEM = {'album_id': '11111111',
                             'time_created': datetime.now()
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

    VALID_ARTIST = {
        'id': 88,
        'name': 'Artist 1',
    }

    # TESTS

    def setUp(self) -> None:
        self.artist = Artist.objects.create(**self.VALID_ARTIST)
        self.album = Album.objects.create(**self.VALID_ALBUM)
        self.user = User.objects.create_user(**self.VALID_USER_DATA)
        self.collection_item = Collection.objects.create(**self.VALID_COLLECTION_ITEM, user=self.user, album=self.album)

    # TESTS BELOW

    def test_collection__when_user_unlikes_album_from_collection__must_remove_it_from_there_but_remains_in_albums(self):
        users_collection = Collection.objects.filter(user_id=self.user.pk)
        self.assertListEqual([self.collection_item, ], list(users_collection), )
        # test unlike
        self.client.post('/unlike-album/<album.pk>', follow=True)
        self.assertTrue(users_collection, [])
        self.assertTrue(list(Album.objects.all()), [self.album, ])
