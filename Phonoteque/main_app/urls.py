from django.urls import path

from Phonoteque.main_app.views import view_dashboard, IndexListView, find_album_by_url, save_artist_album_data, \
    find_album_by_title_and_artist, AlbumDetailView, ArtistDiscographyView

urlpatterns = [
    path('', IndexListView.as_view(), name="index_page"),
    path('dashboard/', view_dashboard, name="dashboard"),
    path('find-by-title/', find_album_by_title_and_artist, name='find_album_by_title_and_artist'),
    path('find-by-url', find_album_by_url, name='find_album_by_url'),
    path('save-album/', save_artist_album_data, name="save_artist_album"),
    path('album-details/<int:pk>/', AlbumDetailView.as_view(), name="album_details"),
    path('artist-discography/<int:pk>/', ArtistDiscographyView.as_view(), name="artist-discography"),
]
