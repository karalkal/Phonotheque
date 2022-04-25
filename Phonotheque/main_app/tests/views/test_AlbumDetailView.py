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

    def test_album_details_view__when_searching_non_existing_album__redirect_to_404(self):
        artist = Artist.objects.create(**self.VALID_ARTIST)
        album = Album.objects.create(**self.VALID_ALBUM)

        response = self.client.get(reverse('album_details', kwargs={'pk': 0}))
        self.assertTemplateUsed(response, '404.html')

    def test_album_details_view__when_searching_existing_album__redirect_to_album_details(self):
        artist = Artist.objects.create(**self.VALID_ARTIST)
        album = Album.objects.create(**self.VALID_ALBUM)

        response = self.client.get(reverse('album_details', kwargs={'pk': 11111111}))
        self.assertTemplateUsed(response, 'main_app/album_details.html')
        self.assertEqual(response.status_code, 200)

    def test_album_details_view__when_searching_existing_album__get_correct_context_data(self):
        artist = Artist.objects.create(**self.VALID_ARTIST)
        album = Album.objects.create(**self.VALID_ALBUM)
        user = User.objects.create_user(**self.VALID_USER_DATA)
        # user_2 = User.objects.create_user(**self.VALID_USER_DATA_2)

        response = self.client.get(reverse('album_details', kwargs={'pk': 11111111}))

        self.assertQuerysetEqual([], response.context_data['others_who_liked_it'])
        self.assertFalse(response.context_data['liked_by_current_user'])
        self.assertEqual(str(album), str(response.context_data['album']))
        self.assertEqual(type(CommentForm()), type(response.context_data['form']))

        # collection_item = Collection.objects.create(**self.VALID_COLLECTION_ITEM, user=user)
        # album.collection_set.add(collection_item)
        # response = self.client.get(reverse('album_details', kwargs={'pk': 11111111}))
        # self.assertTrue(response.context_data['liked_by_current_user'])

        # collection_item2 = Collection.objects.create(**self.VALID_COLLECTION_ITEM, user=user_2)
        # self.assertEqual(2, len(response.context_data['others_who_liked_it']))
