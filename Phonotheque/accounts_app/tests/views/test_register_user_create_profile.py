from datetime import date

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from Phonotheque.accounts_app.forms import UserRegistrationForm
from Phonotheque.accounts_app.models import Profile


class ProfileCreateViewTests(TestCase):
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
        'description': 'some amazing description',
    }

    def setUp(self) -> None:
        self.user = User.objects.create(**self.VALID_USER_DATA)
        self.profile = Profile.objects.create(**self.VALID_PROFILE_DATA, user=self.user)

    def test_get_register_view__should_render_correct_template(self):
        response = self.client.get('')
        self.assertTemplateUsed(response, 'main_app/index.html')
        self.assertTemplateUsed(reverse('index_page'))

    def test_user_and_profile_creation__with_valid_data__expect_ids_to_be_equal(self):
        # test profile
        self.assertEqual(self.profile.user_id, self.user.pk)

    def test_create_user__with_one_char_first_name__raises_error_from_form(self):
        invalid_firts_name_data = {
            'username': "username",
            'email': "baba@baba.com",
            'first_name': "A",
            'last_name': "good Lastname",
            'password': "123jgfhtehkjchj!!!!!!JHAJHSJHJHS",
            'password2': "123jgfhtehkjchj!!!!!!JHAJHSJHJHS",
        }

        invalid_form = UserRegistrationForm(invalid_firts_name_data)
        try:
            new_user = invalid_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(invalid_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
        except ValueError as ex:
            self.assertIsNotNone(ex)
            self.assertEqual("The User could not be created because the data didn't validate.", str(ex))

    def test_post_invalid_user_creation_form__with_one_char_first_name__raises(self):
        INVALID_FIRST_NAME_DATA = {
            'username': "username",
            'email': "baba@baba.com",
            'first_name': "A",
            'last_name': "good Lastname",
            'password': "123jgfhtehkjchj!!!!!!JHAJHSJHJHS",
            'password2': "123jgfhtehkjchj!!!!!!JHAJHSJHJHS",
        }

        invalid_form = UserRegistrationForm(INVALID_FIRST_NAME_DATA)

        with self.assertRaises(Exception) as context:
            new_user = invalid_form.save(commit=False)
            new_user.set_password(invalid_form.cleaned_data['password'])
            new_user.save()
            self.assertIsNone(User.objects.all())



