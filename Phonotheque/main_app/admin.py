from django.contrib import admin

from Phonotheque.main_app.models import Album, Artist, Collection, Comment


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ('name', 'discography')

    @staticmethod
    def discography(obj):
        return "; ".join([lp.title for lp in obj.album_set.all()])


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'shared_by',)


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ('album_id', 'user_id')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'album', 'created', 'active',)
    list_filter = ('active', 'created',)
