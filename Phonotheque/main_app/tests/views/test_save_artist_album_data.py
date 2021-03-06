from datetime import datetime

from django import test as django_test
from django.contrib.auth import get_user_model

from Phonotheque.main_app.models import Collection, Comment, Album, Artist

User = get_user_model()


class ArtistAndAlbumDataSaveTests(django_test.TestCase):
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

    def test_collection__when_user_has_no_collection_items__collection_must_be_empty(self):
        user = self.__create_valid_user()
        users_collection = Collection.objects.filter(user_id=user.pk)
        self.assertListEqual([], list(users_collection), )

    def test_collection__when_user_has_collection_items__collection_must_contain_album(self):
        user = self.__create_valid_user()
        album = self.__create_album(**self.VALID_ALBUM)
        collection_item = self.__create_collection_item_for_user(user, album)

        users_collection = Collection.objects.filter(user_id=user.pk)
        self.assertListEqual([collection_item, ], list(users_collection), )

    def test_album__when_album__is_created__artist_must_be_created_too(self):
        album = self.__create_album(**self.VALID_ALBUM)
        artist = Artist.objects.get(pk=album.artist.pk)
        self.assertEqual(artist, album.artist)

    def test_artist__when_artist_exists__no_error_raised_albums_must_be_saved_and_related_to_same_artist(self):
        artist = self.__create_artist()
        album1 = Album.objects.create(wiki_id=11111111, title='Album1', wiki_url='https://en.album1.org',
                                      summary='studio album 1', resume='Nothing1',
                                      album_cover='https://upload.wikimedia.org/cover1.jpg',
                                      time_created=datetime.now(),
                                      artist_id=88, artist=artist)

        album2 = Album.objects.create(wiki_id=22222222, title='Album2', wiki_url='https://en.album2.org',
                                      summary='studio album 2', resume='Nothing1',
                                      album_cover='https://upload.wikimedia.org/cover2.jpg',
                                      time_created=datetime.now(),
                                      artist_id=88, artist=artist)

        # comparing the Querysets directly results in non-equal, need to be either ordered=False or cast to lists
        albums_by_this_artist_retrieved = Album.objects.filter(artist_id=artist.pk)
        artists_album_set = artist.album_set.all()
        self.assertQuerysetEqual(albums_by_this_artist_retrieved, artists_album_set, ordered=False)
