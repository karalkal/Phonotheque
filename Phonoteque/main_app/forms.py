from django import forms

from Phonoteque.main_app.models import Album, Artist, Comment


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


class CommentForm(forms.ModelForm):
    body = forms.CharField(
        max_length=620,
        label='',
        widget=forms.Textarea(attrs={
            'class': "form-control rounded-0",
            'placeholder': "Share your thoughts, man",
            'required': True,
            'rows': 8}))

    class Meta:
        model = Comment
        fields = ('body',)
