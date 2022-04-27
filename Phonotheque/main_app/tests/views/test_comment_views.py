from datetime import datetime

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from Phonotheque.main_app.models import Artist, Album, Comment


class CommentViewsTests(TestCase):
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
        'is_superuser': True,
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

    VALID_COMMENT = {
        'body': 'The best comment ever',
        'created': datetime.now(),
        'active': True
    }

    # TESTS

    def setUp(self) -> None:
        self.artist = Artist.objects.create(**self.VALID_ARTIST)
        self.album = Album.objects.create(**self.VALID_ALBUM)
        self.user_1 = User.objects.create_user(**self.VALID_USER_DATA)
        self.user_2 = User.objects.create_user(**self.VALID_USER_DATA_2)
        self.comment = Comment.objects.create(**self.VALID_COMMENT, user=self.user_1, album=self.album)

    def test_create_comment_view__expect_correct_template(self):
        response = self.client.get(reverse('album_details', kwargs={'pk': 11111111}))
        self.assertTemplateUsed(response, 'main_app/album_details.html')
        self.assertEqual(response.status_code, 200)

    def test_comment__when_user_has_active_comments__comments_must_exist(self):
        users_comments = Comment.objects.filter(user_id=self.user_1.pk)
        self.assertIn(self.comment, users_comments)

    def test_comment__when_user_has_no_active_comments__comments_queryset_must_be_empty(self):
        users_comments = Comment.objects.filter(user_id=self.user_2.pk)
        self.assertTrue(len(users_comments) == 0)

    def test_comment__when_comments_exist__must_be_related_to_correct_album(self):
        album2 = Album.objects.create(wiki_id=22222222, title='Album2', wiki_url='https://en.album2.org',
                                      summary='studio album 2', resume='Nothing1',
                                      album_cover='https://upload.wikimedia.org/cover2.jpg',
                                      time_created=datetime.now(),
                                      artist_id=88, artist=self.artist)

        comment2 = Comment.objects.create(**self.VALID_COMMENT, user=self.user_2, album=self.album)
        should_not_display_comment = Comment.objects.create(**self.VALID_COMMENT, user=self.user_2, album=album2)

        comments_to_album_1 = Comment.objects.filter(album_id=self.album.pk)
        self.assertIn(self.comment, list(comments_to_album_1))
        self.assertIn(comment2, list(comments_to_album_1))
        self.assertNotIn(should_not_display_comment, list(comments_to_album_1))
        self.assertIn(should_not_display_comment,
                      Comment.objects.all())  # it is in all() but not in album1's comments
        self.assertEqual(len(Comment.objects.all()), 3)

    def test_comment__when_comments_exist__must_be_related_to_correct_user(self):
        album2 = Album.objects.create(wiki_id=22222222, title='Album2', wiki_url='https://en.album2.org',
                                      summary='studio album 2', resume='Nothing1',
                                      album_cover='https://upload.wikimedia.org/cover2.jpg',
                                      time_created=datetime.now(),
                                      artist_id=88, artist=self.artist)
        comment2 = Comment.objects.create(**self.VALID_COMMENT, user=self.user_1, album=album2)
        should_not_display_comment = Comment.objects.create(**self.VALID_COMMENT, user=self.user_2, album=album2)

        comments_by_user_1 = Comment.objects.filter(user_id=self.user_1.pk)
        self.assertIn(self.comment, list(comments_by_user_1))
        self.assertIn(comment2, list(comments_by_user_1))
        self.assertNotIn(should_not_display_comment, list(comments_by_user_1))
        self.assertIn(should_not_display_comment,
                      Comment.objects.all())  # it is in all() but not in user1's comments
        self.assertEqual(len(Comment.objects.all()), 3)

    def test_delete_comment(self):
        user_data = {'username': 'test_user', 'password': '11111111', }
        self.client.login(**user_data)

        self.assertEqual(len(Comment.objects.all()), 1)

        comment_to_delete = Comment.objects.first()

        self.client.get(
            reverse('delete_comment', kwargs={'comment_pk': comment_to_delete.pk, 'album_wiki_id': 11111111}))
        self.assertEqual(len(Comment.objects.all()), 0)

    def test_disable_comment(self):
        user_data = {'username': 'test_user', 'password': '11111111', }
        self.client.login(**user_data)

        self.assertEqual(len(Comment.objects.all()), 1)

        comment_to_disable = Comment.objects.first()
        self.assertTrue(comment_to_disable.active)

        self.client.get(
            reverse('disable_comment', kwargs={'comment_pk': comment_to_disable.pk, 'album_wiki_id': 11111111}))

        self.assertFalse(Comment.objects.first().active)
