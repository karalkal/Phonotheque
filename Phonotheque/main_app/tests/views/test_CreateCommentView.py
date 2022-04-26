from datetime import datetime

from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from Phonotheque.main_app.forms import CommentForm
from Phonotheque.main_app.models import Artist, Album, Collection, Comment


class AlbumDetailViewTests(TestCase):
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

    def test_create_comment_view__expect_correct_template(self):
        user = self.__create_valid_user()
        artist = self.__create_artist()
        album = Album.objects.create(wiki_id=11111111, title='Album1',
                                     wiki_url='https://en.album1.org',
                                     summary='studio album 1', resume='Nothing1',
                                     album_cover='https://upload.wikimedia.org/cover1.jpg',
                                     time_created=datetime.now(),
                                     artist=artist)
        comment = self.__create_comment_for_album_by_user(user, album)

        response = self.client.get(reverse('album_details', kwargs={'pk': 11111111}))
        self.assertTemplateUsed(response, 'main_app/album_details.html')
        self.assertEqual(response.status_code, 200)

    def test_comment__when_user_has_no_active_comments__comments_must_be_empty(self):
        user = self.__create_valid_user()
        users_comments = Comment.objects.filter(user_id=user.pk)
        self.assertListEqual([], list(users_comments), )

    def test_comment__when_comments_exist__must_be_related_to_correct_album(self):
        user1 = self.__create_valid_user()
        user2 = User.objects.create(
            username="another_user",
            password='11111111',
            email="test2@user.com",
            first_name='Testis',
            last_name='Useless',
        )
        artist = self.__create_artist()
        album1 = Album.objects.create(wiki_id=11111111, title='Album1',
                                      wiki_url='https://en.album1.org',
                                      summary='studio album 1', resume='Nothing1',
                                      album_cover='https://upload.wikimedia.org/cover1.jpg',
                                      time_created=datetime.now(),
                                      artist_id=88, artist=artist)

        album2 = Album.objects.create(wiki_id=22222222, title='Album2', wiki_url='https://en.album2.org',
                                      summary='studio album 2', resume='Nothing1',
                                      album_cover='https://upload.wikimedia.org/cover2.jpg',
                                      time_created=datetime.now(),
                                      artist_id=88, artist=artist)
        comment1 = self.__create_comment_for_album_by_user(user1, album1)
        comment2 = self.__create_comment_for_album_by_user(user2, album1)
        should_not_display_comment = self.__create_comment_for_album_by_user(user2, album2)

        comments = Comment.objects.filter(album_id=album1.pk)
        self.assertIn(comment1, list(comments))
        self.assertIn(comment2, list(comments))
        self.assertNotIn(should_not_display_comment, list(comments))
        self.assertIn(should_not_display_comment, Comment.objects.all())  # it is in all() but not in album1's comments

    def test_comment__when_comments_exist__must_be_related_to_correct_user(self):
        user1 = self.__create_valid_user()
        user2 = User.objects.create(
            username="another_user",
            password='11111111',
            email="test2@user.com",
            first_name='Testis',
            last_name='Useless',
        )
        artist = self.__create_artist()
        album1 = Album.objects.create(wiki_id=11111111, title='Album1',
                                      wiki_url='https://en.album1.org',
                                      summary='studio album 1', resume='Nothing1',
                                      album_cover='https://upload.wikimedia.org/cover1.jpg',
                                      time_created=datetime.now(),
                                      artist_id=88, artist=artist)

        album2 = Album.objects.create(wiki_id=22222222, title='Album2', wiki_url='https://en.album2.org',
                                      summary='studio album 2', resume='Nothing1',
                                      album_cover='https://upload.wikimedia.org/cover2.jpg',
                                      time_created=datetime.now(),
                                      artist_id=88, artist=artist)
        comment1 = self.__create_comment_for_album_by_user(user1, album1)
        comment2 = self.__create_comment_for_album_by_user(user1, album2)
        should_not_display_comment = self.__create_comment_for_album_by_user(user2, album2)

        comments = Comment.objects.filter(user_id=user1.pk)
        self.assertIn(comment1, list(comments))
        self.assertIn(comment2, list(comments))
        self.assertNotIn(should_not_display_comment, list(comments))
        self.assertIn(should_not_display_comment, Comment.objects.all())  # it is in all() but not in user1's comments
