from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.db import IntegrityError
from django.db.models import Count
from django.shortcuts import render, redirect
from django.views import generic as views
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from Phonoteque.common_funcs.db_crud_actions import get_all_artists_names, get_artist_object_by_name, \
    create_album_object
from Phonoteque.common_funcs.wiki_album_finder import get_wiki_info_by_album_name, get_wiki_info_from_url
from Phonoteque.main_app.forms import SearchAlbumForm
from Phonoteque.main_app.models import Artist, Album, Collection


class IndexListView(views.ListView):
    model = Album
    template_name = 'main_app/index.html'
    paginate_by = 8
    context_object_name = 'all_albums'


class AlbumDetailView(views.DetailView):
    model = Album
    template_name = 'main_app/album_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_fans = User.objects. \
            filter(collection__album__wiki_id=self.object.wiki_id). \
            select_related('profile')  # we get the related profile data as well
        # find other users who liked it
        context['others_who_liked_it'] = all_fans.exclude(username=self.request.user.username)

        # find out is current user has shared it too
        try:
            all_fans.get(username=self.request.user.username)
            context['liked_by_current_user'] = True
        except User.DoesNotExist:
            context['liked_by_current_user'] = False

        # TODO add album and artist data to context, so it can be passed to save_artist_album if user wants to add it to their Favourites

        return context


class ArtistDiscographyView(views.ListView):
    model = Album
    template_name = 'main_app/artist_details.html'
    paginate_by = 8

    def get_queryset(self):  # get queryset/albums_list for this specific artist
        return super(ArtistDiscographyView, self).get_queryset() \
            .filter(artist_id=self.kwargs['pk'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ArtistDiscographyView, self).get_context_data()
        artist = Artist.objects.get(pk=self.kwargs['pk'])
        context['artist_name'] = artist.name
        return context


@login_required
def view_dashboard(request):
    # Get user's favourite albums and enable pagination
    object_list = Album.objects. \
        annotate(count=Count('fans')).order_by('count'). \
        filter(collection__user_id=request.user.pk). \
        annotate(count=Count('fans')). \
        order_by('-count', '-time_created', )

    paginator = Paginator(object_list, 4)  # 4 albums in each page
    page = request.GET.get('page')

    try:
        fav_albums = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        fav_albums = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        fav_albums = paginator.page(paginator.num_pages)

    # Display search forms
    form = SearchAlbumForm()
    return render(request, 'main_app/dashboard.html',
                  {'is_paginated': True,
                   'page_obj': page,
                   'fav_albums': fav_albums,
                   'form': form, })


def find_album_by_title_and_artist(request):
    if request.method == 'POST':
        album_name = request.POST['album_name'].title()

        # Search by album name only first
        search_term = album_name
        album_wiki_info, artist_name = get_wiki_info_by_album_name(search_term)

        # If album info has NOT been retrieved from Wiki by album name only, use user entry for artist too
        if not artist_name or not album_wiki_info:
            searched_artist = request.POST['artist_name'].title()
            search_term = album_name + " " + searched_artist
            album_wiki_info, artist_name = get_wiki_info_by_album_name(search_term)

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
        else:
            messages.warning(request, f"We couldn't find an album called {album_name} by {searched_artist}.")
            return redirect('dashboard')


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
        else:
            messages.warning(request, "The link you have provided does not return a valid result.")
            return redirect('dashboard')


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
        this_guys_albums = Album.objects.filter(collection__user_id=request.user.pk)

        # unique_together from Collection will throw an error anyway, this is level 1 verification
        if this_guys_albums.filter(wiki_id=album.wiki_id).exists():
            messages.warning(request, f'The Album {album.title} by {album.artist} is already in your favourites')
            return redirect('dashboard')

    # if not function will create album object
    except ObjectDoesNotExist:
        album = create_album_object(album_wiki_info, artist_object, )
        # Need to save it first, so that Collection can use its wiki_id
        album.save()

    # identify relevant user
    user = request.user

    # then save via Collection intermediary model
    try:
        Collection.objects.create(
            user=user,
            album=album)

    # Not needed, just to see which error is coming from where, will be caught before reaching the DB, see above
    except IntegrityError:
        messages.warning(request, 'An user cannot save the same album twice')
        return redirect('dashboard')

    return render(request, 'main_app/album_saved.html',
                  {'album': album})
