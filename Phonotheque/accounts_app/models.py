from django.db import models
from django.conf import settings


class Profile(models.Model):
    MALE_GENDER = ("Male", "Male")
    FEMALE_GENDER = ("Female", "Female")
    DO_NOT_SHOW_GENDER = ("Do not show", "Do not show")
    GENDER_CHOICES = [MALE_GENDER, FEMALE_GENDER, DO_NOT_SHOW_GENDER]

    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                primary_key=True)

    # The user may provide the following information in their profile:
    photo_URL = models.URLField(null=True, blank=True, max_length=1024)
    # Heroku/Cloudinary say 'add credit card for verification', I say F*** off
    # email = models.EmailField(null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(
        max_length=max([len(x) for (x, _) in GENDER_CHOICES]),
        null=True, blank=True,
        choices=GENDER_CHOICES,
        default=DO_NOT_SHOW_GENDER[1],
    )
    description = models.TextField(null=True, blank=True)


def __str__(self):
    return f"{self.first_name} {self.last_name}"
