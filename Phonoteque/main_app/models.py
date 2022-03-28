from django.contrib.auth.models import User
from django.db import models


class Artist(models.Model):
    name = models.CharField(max_length=35)

    def __str__(self):
        return f"{self.name}"


class Album(models.Model):
    wiki_id = models.CharField(max_length=35, primary_key=True)  # PRIMARY KEY IS WIKI ID
    artist = models.ForeignKey(to=Artist,
                               on_delete=models.CASCADE)  # Foreign Key - probably won't be needed unless admin deletes Artist from DB
    fans = models.ManyToManyField(User, through='Collection')
    title = models.CharField(max_length=35)
    wiki_url = models.URLField()
    summary = models.TextField(null=True, blank=True, )
    resume = models.TextField(null=True, blank=True, )
    album_cover = models.URLField()
    time_created = models.DateTimeField(auto_now_add=True)

    @property
    def shared_by(self):
        # get data for album from intermediary model, i.e. users linked to same album id
        album_fans = User.objects.filter(collection__album__wiki_id=self.wiki_id)
        return album_fans

    # class Meta:
    #     ordering = ('-time_created',)

    def __str__(self):
        return f"{self.title} by \n{self.artist}"


class Collection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    time_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-time_created',)
        unique_together = ('user', 'album')

    def __str__(self):
        return f"{self.user.username} --> {self.album.title} - {self.album.artist.name}"
