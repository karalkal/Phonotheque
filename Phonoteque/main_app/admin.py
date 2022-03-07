from django.contrib import admin

from Phonoteque.main_app.models import Album, Artist


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ('name', 'discography')

    def discography(self, obj):
        return ", ".join([lp.title for lp in obj.album_set.all()])


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist')
