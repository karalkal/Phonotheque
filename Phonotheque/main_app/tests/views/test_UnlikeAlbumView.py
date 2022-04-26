from datetime import datetime

from django import test as django_test
from django.contrib.auth import get_user_model

from Phonotheque.main_app.models import Collection, Comment, Album, Artist

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
    VALID_COMMENT = {
        'body': 'The best comment ever',
        'created': datetime.now(),
        'active': True
        # album_id
        # user_id
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

    def __create_valid_user(self):
        new_user = User.objects.create_user(**self.VALID_USER_DATA)
        return new_user

    def __create_collection_item_for_user(self, user, album):
        collection_item = Collection.objects.create(**self.VALID_COLLECTION_ITEM, user=user)
        return collection_item

    def __create_comment_for_album_by_user(self, user, album):
        comment = Comment.objects.create(**self.VALID_COMMENT, user=user, album=album)
        return comment

    def __create_artist(self):
        artist = Artist.objects.create(**self.VALID_ARTIST)
        return artist

    def __create_album(self, **kwargs):
        artist = self.__create_artist()
        new_album = Album.objects.create(**kwargs, artist=artist)
        return new_album

    # TESTS BELOW

    def test_collection__when_user_unlikes_album_from_collection__must_remove_it_from_there_but_remains_in_albums(self):
        # create scenario
        album = self.__create_album(**self.VALID_ALBUM)
        user = self.__create_valid_user()
        collection_item = self.__create_collection_item_for_user(user, album)
        users_collection = Collection.objects.filter(user_id=user.pk)
        self.assertListEqual([collection_item, ], list(users_collection), )
        # test unlike
        self.client.post('/unlike-album/<album.pk>', follow=True)
        self.assertTrue(users_collection, [])
        self.assertTrue(list(Album.objects.all()), [album, ])
