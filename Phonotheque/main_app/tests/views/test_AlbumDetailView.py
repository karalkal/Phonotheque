from datetime import datetime

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from Phonotheque.main_app.forms import CommentForm
from Phonotheque.main_app.models import Artist, Album, Collection


class AlbumDetailViewTests(TestCase):
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

    def test_album_details_view__when_searching_non_existing_album__redirect_to_404(self):
        response = self.client.get(reverse('album_details', kwargs={'pk': 0}))
        self.assertTemplateUsed(response, '404.html')

    def test_album_details_view__when_searching_existing_album__redirect_to_album_details(self):
        response = self.client.get(reverse('album_details', kwargs={'pk': 11111111}))
        self.assertTemplateUsed(response, 'main_app/album_details.html')
        self.assertEqual(response.status_code, 200)

    def test_album_details_view__get_correct_context_data(self):
        response = self.client.get(reverse('album_details', kwargs={'pk': 11111111}))

        self.assertQuerysetEqual([], response.context_data['others_who_liked_it'])
        self.assertFalse(response.context_data['liked_by_current_user'])
        self.assertEqual(str(self.album), str(response.context_data['album']))
        self.assertEqual(type(CommentForm()), type(response.context_data['form']))

    def test_album_details_view__when_liked_by_non_logged__get_correct_value_in_context_data(self):
        Collection.objects.create(user=self.user, album=self.album)
        Collection.objects.create(user=self.user_2, album=self.album)

        response = self.client.get(reverse('album_details', kwargs={'pk': 11111111}))

        self.assertListEqual(list(self.album.shared_by), list(response.context_data['others_who_liked_it']))

    def test_album_details_view__when_liked_by_logged_in_user__get_correct_value_in_context_data(self):
        Collection.objects.create(user=self.user, album=self.album)
        Collection.objects.create(user=self.user_2, album=self.album)
        user_data = {'username': 'test_user', 'password': '11111111', }

        self.client.login(**user_data)

        response = self.client.get(reverse('album_details', kwargs={'pk': 11111111}))

        self.assertEqual(1, len(response.context_data['others_who_liked_it']))
        self.assertTrue(response.context_data['liked_by_current_user'])

