from datetime import date

from django import test as django_test
from django.contrib.auth import get_user_model

from Phonotheque.accounts_app.models import Profile

User = get_user_model()


class UserAndProfileEditTests(django_test.TestCase):
    VALID_USER_DATA = {
        'username': "test_user",
        'password': '11111111',
        'email': "test@user.com",
        'first_name': 'Test',
        'last_name': 'User',
    }

    VALID_PROFILE_DATA = {
        'date_of_birth': date(1988, 4, 13),
        'photo_URL': 'https://cdn.pixabay.com/photo/2017/05/11/08/48/woman-2303361_960_720.jpg',
        'gender': 'Male',
        'description': 'some amazing description'
    }

    def __create_valid_user_and_profile(self):
        new_user = User.objects.create_user(**self.VALID_USER_DATA)
        new_profile = Profile.objects.create(
            user=new_user,
            **self.VALID_PROFILE_DATA
        )
        return new_user, new_profile

    # tests

    def test_when_editing_user_data__expect_updated_values(self):
        user, profile = self.__create_valid_user_and_profile()
        user.first_name = "New name"
        self.assertEqual("New name", user.first_name)
