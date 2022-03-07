from Phonoteque.main_app.models import Artist


def get_all_artists_names():
    return [artist.name for artist in Artist.objects.all()]


def get_artist_object_by_name(artist_name):
    return Artist.objects.get(name=artist_name)
