from django.core.validators import MinLengthValidator, RegexValidator
from django.db import models

from Phonoteque.main_app.validators import CheckMaxSizeInMb


class Profile(models.Model):
    MALE_GENDER = ("Male", "Male")
    FEMALE_GENDER = ("Female", "Female")
    DO_NOT_SHOW_GENDER = ("Do not show", "Do not show")
    GENDER_CHOICES = [MALE_GENDER, FEMALE_GENDER, DO_NOT_SHOW_GENDER]
    VALID_NAME_REGEX = r"^([ \u00c0-\u01ffa-zA-Z'\-])+$"  # Jérémie O'Conor-IVANOVäüïöëÿâçéèêîïôčšžñáéíóúü
    INVALID_NAME_ERROR_MESSAGE = "This name format won't work."
    first_name = models.CharField(max_length=35, validators=(
        MinLengthValidator(2),
        RegexValidator(regex=VALID_NAME_REGEX, message=INVALID_NAME_ERROR_MESSAGE))
                                  )
    last_name = models.CharField(max_length=35, validators=(
        MinLengthValidator(2),
        RegexValidator(regex=VALID_NAME_REGEX, message=INVALID_NAME_ERROR_MESSAGE))
                                 )
    profile_picture = models.ImageField(
        upload_to='images',
        # validators=validate_max_size
    )

    # The user may provide the following information in their profile:
    profile_image = models.ImageField(
        null=True,
        blank=True,
        upload_to='profile_images/',
        validators=(CheckMaxSizeInMb,),
    )
    date_of_birth = models.DateField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    gender = models.CharField(max_length=max([len(x) for (x, _) in GENDER_CHOICES]),
                              null=True, blank=True,
                              choices=GENDER_CHOICES,
                              default=DO_NOT_SHOW_GENDER[1],
                              )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Artist(models.Model):
    name = models.CharField(max_length=35)

    def __str__(self):
        return f"{self.name}"


class Album(models.Model):
    wiki_id = models.CharField(max_length=35, primary_key=True)
    title = models.CharField(max_length=35)
    album_cover = models.URLField()
    summary = models.TextField(null=True, blank=True, )
    artist = models.ForeignKey(to=Artist, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} by \n{self.artist}"
