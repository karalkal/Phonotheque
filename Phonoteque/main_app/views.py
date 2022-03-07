from django.shortcuts import render, HttpResponse, redirect

from Phonoteque.common_funcs.get_album_artist_data_from_db import get_all_artists_names, get_artist_object_by_name
from Phonoteque.common_funcs.wiki_album_finder import get_wiki_info
from Phonoteque.main_app.forms import CreateAlbumForm, SearchAlbumForm
from Phonoteque.main_app.models import Artist, Album


def index_view(request):
    pass


def search_form_view(request):
    if request.method == 'POST':
        album_name = request.POST['album_name'].title()
        artist_name = request.POST['artist_name'].title()
        search_term = album_name + " " + artist_name
        album_wiki_info = get_wiki_info(search_term)

        # If album info has been retrieved from Wiki
        if album_wiki_info:
            # Check if artist already in DB, if not create record
            if artist_name not in get_all_artists_names():
                new_artist = Artist.objects.create(name=artist_name)  # create and save directly

            artist_object = get_artist_object_by_name(artist_name)

            # first create album object, then save it
            album = Album(
                wiki_id=album_wiki_info['wiki_id'],
                title=album_wiki_info['wiki_title'],
                album_cover=album_wiki_info['wiki_image'],
                summary=album_wiki_info['wiki_summary'],
                artist=artist_object,  # artist is an object
                # html=album_wiki_info['wiki_html']
            )
            album.save()

            return render(request, 'main_app/album_saved.html',
                          {'album': album})

        # TODO If no info, display message and display form again
    else:
        form = SearchAlbumForm()
    return render(request, 'main_app/album_search.html',
                  {'form': form})
