from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, HttpResponse, redirect
from django.views.generic import ListView

from Phonoteque.common_funcs.db_crud_actions import get_all_artists_names, get_artist_object_by_name, \
    create_album_object
from Phonoteque.common_funcs.wiki_album_finder import get_wiki_info, get_wiki_info_from_url
from Phonoteque.main_app.forms import CreateAlbumForm, SearchAlbumForm
from Phonoteque.main_app.models import Artist, Album, Collection


class IndexListView(ListView):
    model = Album
    template_name = 'main_app/index.html'


@login_required
def view_dashboard(request):
    if request.method == 'POST':
        album_name = request.POST['album_name'].title()

        # Search by album name only first
        search_term = album_name
        album_wiki_info, artist_name = get_wiki_info(search_term)

        # If album info has NOT been retrieved from Wiki by album name only, use user entry for artist too
        if not artist_name or not album_wiki_info:
            artist_name = request.POST['artist_name'].title()
            search_term = album_name + " " + artist_name
            album_wiki_info, artist_name = get_wiki_info(search_term)

        # Check if artist already in DB, if not create record
        if artist_name not in get_all_artists_names():
            Artist.objects.create(name=artist_name)  # create and save directly

        # obtain artist from DB to create FK relation in album
        artist_object = get_artist_object_by_name(artist_name)

        # if album exists in DB already
        try:
            album = Album.objects.get(wiki_id=album_wiki_info['wiki_id'])
            # TODO: If user has added album already, do nothing ==== DONE BUT CHECK
            if Collection.objects.filter(user_id=request.user.pk):
                return redirect('dashboard')

        # if not function will create album object
        except ObjectDoesNotExist:
            album = create_album_object(album_wiki_info, artist_object, )
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
    else:  # just display user's favourite albums + search forms
        fav_albums = Album.objects.filter(collection__user_id=request.user.pk)
        form = SearchAlbumForm()
        return render(request, 'main_app/dashboard.html',
                      {'fav_albums': fav_albums,
                       'form': form, })


def find_album_by_url(request):
    if request.method == 'POST':
        album_url = request.POST['message']
        album_wiki_info, artist_name = get_wiki_info_from_url(album_url)

        # Save the data in the session - is that alright?
        request.session['data'] = artist_name, album_wiki_info
        if album_wiki_info and artist_name:
            context = {'artist': artist_name,
                       'title': album_wiki_info['wiki_title'],
                       'summary': album_wiki_info['wiki_summary'],
                       'cover_image': album_wiki_info['wiki_image']
                       }
            return render(request,
                          'main_app/found_album.html', context)


def save_artist_album_data(request):
    artist_name, album_wiki_info = request.session['data']
    del request.session['data']  # clear this value

    # Check if artist already in DB, if not create record
    if artist_name not in get_all_artists_names():
        Artist.objects.create(name=artist_name)  # create and save directly

    # obtain artist from DB to create FK relation in album
    artist_object = get_artist_object_by_name(artist_name)

    # if album exists in DB already
    try:
        album = Album.objects.get(wiki_id=album_wiki_info['wiki_id'])
        # TODO: If user has added album already, do nothing ==== DONE BUT CHECK
        if Collection.objects.filter(user_id=request.user.pk):
            return redirect('dashboard')

    # if not function will create album object
    except ObjectDoesNotExist:
        album = create_album_object(album_wiki_info, artist_object, )
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
