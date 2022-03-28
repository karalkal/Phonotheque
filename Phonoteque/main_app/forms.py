from django import forms

from Phonoteque.main_app.models import Album, Artist


class SearchAlbumForm(forms.Form):
    artist_name = forms.CharField(
        max_length=35,
        label="",
        widget=forms.TextInput(attrs={
            'name': "artist_name",
            'class': "form-control rounded-0",
            'placeholder': "Enter Artist Name",
            'required': True, }))

    album_name = forms.CharField(
        max_length=80,
        label="",
        widget=forms.TextInput(attrs={
            'name': "album_name",
            'class': "form-control rounded-0",
            'placeholder': "Enter Album Name",
            'required': True, }))


# class CreateArtistForm(forms.ModelForm):
#     class Meta:
#         model = Artist
#         fields = '__all__'
#
#
# class CreateAlbumForm(forms.ModelForm):
#     class Meta:
#         model = Album
#         fields = '__all__'
