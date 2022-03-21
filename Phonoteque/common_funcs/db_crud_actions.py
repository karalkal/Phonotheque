from Phonoteque.main_app.models import Artist, Album


def get_all_artists_names():
    return [artist.name for artist in Artist.objects.all()]


def get_artist_object_by_name(artist_name):
    return Artist.objects.get(name=artist_name)


def create_album_object(album_wiki_info, artist_object):
    new_album = Album(
        wiki_id=album_wiki_info['wiki_id'],
        artist=artist_object,  # artist is an object
        title=album_wiki_info['wiki_title'],
        wiki_url=album_wiki_info['wiki_url'],
        summary=album_wiki_info['wiki_summary'],
        resume=album_wiki_info['wiki_resume'],
        album_cover=album_wiki_info['wiki_image'],
    )
    return new_album
