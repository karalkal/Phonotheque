from datetime import date

from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from Phonotheque.accounts_app.models import Profile


class CustomPasswordChangeViewTests(TestCase):
    VALID_USER_DATA = {
        'username': "Ivancho",
        'password': '11111111',
        'email': "ivanushka@user.com",
        'first_name': 'Ivanushka',
        'last_name': 'Glupaka',
        'is_staff': False,
    }

    VALID_PROFILE_DATA = {
        'date_of_birth': date(1988, 4, 13),
        'photo_URL': 'https://cdn.pixabay.com/photo/2017/05/11/08/48/woman-2303361_960_720.jpg',
        'gender': 'Male',
        'description': 'some amazing description',
    }

    def setUp(self) -> None:
        self.user = User.objects.create(**self.VALID_USER_DATA)
        self.user = Profile.objects.create(**self.VALID_PROFILE_DATA, user=self.user)

        # TESTS

    def test_password_change_form_formatting(self):
        user_data = {'username': 'BayHuy', 'password': '11111111', }
        self.client.login(**user_data)

        self.client.get(reverse('password-change'))

        self.assertEqual(list(PasswordChangeForm(self.user, {}).fields),
                         ['old_password', 'new_password1', 'new_password2'])

        form = PasswordChangeForm(self.user, {
            'old_password': "11",
            'new_password1': "22",
            'new_password2': "22"
        })

        for (field_name, field) in form.fields.items():
            self.assertTrue(field.widget.attrs['class'] == "form-control")
            self.assertTrue(field.widget.attrs['placeholder'] == f"Enter {field_name.title()}")

        # field.widget.attrs['class'] = "form-control"
