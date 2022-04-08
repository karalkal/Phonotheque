from django.urls import path

from Phonotheque.main_app.views import view_dashboard, IndexListView, find_album_by_url, save_artist_album_data, \
    find_album_by_title_and_artist, AlbumDetailView, ArtistDiscographyView, add_shared_album_to_own_collection, \
    CommentCreateView, AboutView, UnlikeAlbumView

urlpatterns = [
    path('', IndexListView.as_view(), name="index_page"),
    path('dashboard/', view_dashboard, name="dashboard"),
    path('find-by-title/', find_album_by_title_and_artist, name='find_album_by_title_and_artist'),
    path('find-by-url', find_album_by_url, name='find_album_by_url'),
    path('save-album/', save_artist_album_data, name="save_artist_album"),
    path('save-shared-album/<int:album_wiki_id>/', add_shared_album_to_own_collection, name="save_shared_album"),
    path('album-details/<int:pk>/', AlbumDetailView.as_view(), name="album_details"),
    path('unlike-album/<int:pk>/', UnlikeAlbumView.as_view(), name="unlike_album"),
    path('artist-discography/<int:pk>/', ArtistDiscographyView.as_view(), name="artist-discography"),
    path('post-comment/<int:album_wiki_id>/', CommentCreateView.as_view(), name="post_comment"),
    path('about/', AboutView.as_view(), name="about_page"),
]
