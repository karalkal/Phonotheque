from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, HttpResponse, redirect
from django.views.generic import ListView

from Phonoteque.common_funcs.db_crud_actions import get_all_artists_names, get_artist_object_by_name, \
    create_album_object
from Phonoteque.common_funcs.wiki_album_finder import get_wiki_info
from Phonoteque.main_app.forms import CreateAlbumForm, SearchAlbumForm
from Phonoteque.main_app.models import Artist, Album, Collection


class IndexListView(ListView):
    model = Album
    template_name = 'main_app/index.html'


@login_required
def view_dashboard(request):
    if request.method == 'POST':
        album_name = request.POST['album_name'].title()
        artist_name = request.POST['artist_name'].title()
        search_term = album_name + " " + artist_name
        album_wiki_info = get_wiki_info(search_term)

        # If album info has been retrieved from Wiki
        if album_wiki_info:
            # Check if artist already in DB, if not create record
            if artist_name not in get_all_artists_names():
                Artist.objects.create(name=artist_name)  # create and save directly
            artist_object = get_artist_object_by_name(artist_name)  # then get artist name from DB

            # first create album object, then save it
            album = Album(
                wiki_id=album_wiki_info['wiki_id'],
                artist=artist_object,  # artist is an object
                title=album_wiki_info['wiki_title'],
                wiki_url=album_wiki_info['wiki_url'],
                summary=album_wiki_info['wiki_summary'],
                resume=album_wiki_info['wiki_resume'],
                album_cover=album_wiki_info['wiki_image'],
            )
            album.save()

            return render(request, 'main_app/album_saved.html',
                          {'album': album})

        # TODO If no info, display message and display form again
    else:
        form = SearchAlbumForm()
    return render(request, 'main_app/dashboard.html',
                  {'form': form})


def search_album_view(request):
    if request.method == 'POST':
        album_name = request.POST['album_name'].title()
        artist_name = request.POST['artist_name'].title()
        search_term = album_name + " " + artist_name
        album_wiki_info = get_wiki_info(search_term)

        # If album info has been retrieved from Wiki
        if album_wiki_info:
            # Check if artist already in DB, if not create record
            if artist_name not in get_all_artists_names():
                Artist.objects.create(name=artist_name)  # create and save directly

            # obtain artist from DB to create FK relation in album
            artist_object = get_artist_object_by_name(artist_name)

            # possibly redundant
            if not request.user.is_authenticated:
                return redirect('index_page')

            # if album exists in DB already
            try:
                album = Album.objects.get(wiki_id=album_wiki_info['wiki_id'])
                # TODO: If user has added album already, do nothing
                if Collection.objects.filter(user_id=request.user.pk):
                    return redirect('dashboard')

            # if not function will create album object
            except ObjectDoesNotExist:
                album = create_album_object(album_wiki_info, artist_object)
                # Need to save it first, so that Collection can use its wiki_id
                album.save()

            # identify relevant user
            user = request.user

            # then save via Collection intermediary model
            Collection.objects.create(
                user=user,
                album=album)

            return render(request, 'main_app/album_saved.html',
                          {'album': album})

        # TODO: If no info, display message and display form again
    else:
        form = SearchAlbumForm()
    return render(request, 'main_app/album_search.html',
                  {'form': form})
