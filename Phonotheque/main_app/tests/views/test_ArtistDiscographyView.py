from datetime import datetime

from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory
from django.urls import reverse

from Phonotheque.main_app.forms import CommentForm
from Phonotheque.main_app.models import Artist, Album
from Phonotheque.main_app.views import ArtistDiscographyView


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

    def test_artist_discography_view___redirect_to_artist_page(self):
        artist = Artist.objects.create(**self.VALID_ARTIST)
        album = Album.objects.create(**self.VALID_ALBUM)

        response = self.client.get(reverse('artist-discography', kwargs={'pk': 88}))
        self.assertTemplateUsed(response, 'main_app/artist_details.html')
        self.assertEqual(response.status_code, 200)

    def test_artist_discography_view__when_viewing_artist_page__get_correct_context_data(self):
        artist = Artist.objects.create(**self.VALID_ARTIST)
        album = Album.objects.create(**self.VALID_ALBUM)

        response = self.client.get(reverse('artist-discography', kwargs={'pk': 88}))

        self.assertEqual(artist.name, str(response.context_data['artist_name']))
        self.assertIn(str(album), str(response.context_data['album_list']))

    # def test_artist_discography_view__when_viewing_artist_page__get_correct_queryset(self):
    #     artist = Artist.objects.create(**self.VALID_ARTIST)
    #     album = Album.objects.create(**self.VALID_ALBUM)
    #     request = RequestFactory().get(reverse('artist-discography', kwargs={'pk': 88}))
    #
    #     view = ArtistDiscographyView()
    #     view.setup(request)
    #
    #     context = view.get_context_data()

        assert context['number_of_peaks_completed'] == 7

    # view.object_list = view.get_queryset()
        # context = view.get_context_data()
