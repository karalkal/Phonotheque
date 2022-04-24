from Phonotheque.accounts_app.forms import UserEditForm, ProfileEditForm
from django import test as django_test


class UserRegistrationFormTests(django_test.TestCase):
    valid_user_data = {
        'username': "username",
        'email': "baba@baba.com",
        'first_name': "good Firstname",
        'last_name': "good Lastname",
        'password': "123jgfhtehkjchj!!!!!!JHAJHSJHJHS",
        'password2': "123jgfhtehkjchj!!!!!!JHAJHSJHJHS",
    }

    '''Have to get copy of valid data as otherwise overwrites data in valid_user_data'''

    def test_user_edit_form__with_valid_data__expect_valid_form(self):
        user_form = UserEditForm(self.valid_user_data)
        self.assertTrue(user_form.is_valid())

    def test_user_creation_form__with_prohibited_chars_first_name__raises(self):
        user_form = UserEditForm(self.valid_user_data.copy())
        user_form.data['first_name'] = "Invalid_FirstName"

        # form fails
        self.assertFalse(user_form.is_valid())
        # won't be saved
        with self.assertRaises(Exception) as context:
            user_form.save()
        self.assertEqual("The User could not be created because the data didn't validate.", str(context.exception))
        # display message
        self.assertIn("This name format won't work here, buddy.", user_form.errors['first_name'])

    def test_user_edit_form_field_formatting__expect_to_obtain_formatting_from_mixin(self):
        user_form = UserEditForm(self.valid_user_data.copy())
        for k, v in user_form.fields.items():
            expected_format = 'form-control rounded'
            actual_format = v.widget.attrs['class']
            self.assertEqual(expected_format, actual_format)

            expected_placeholder = f"Enter {k.title().replace('_', ' ')}"
            actual_placeholder = v.widget.attrs['placeholder']
            self.assertEqual(expected_placeholder, actual_placeholder)

    def test_profile_edit_form_field_formatting__expect_to_obtain_formatting_from_mixin(self):
        profile_form = ProfileEditForm(self.valid_user_data.copy())
        for k, v in profile_form.fields.items():
            expected_format = 'form-control rounded'
            actual_format = v.widget.attrs['class']
            self.assertEqual(expected_format, actual_format)

            expected_placeholder = f"Enter {k.title().replace('_', ' ')}"
            actual_placeholder = v.widget.attrs['placeholder']
            self.assertEqual(expected_placeholder, actual_placeholder)
