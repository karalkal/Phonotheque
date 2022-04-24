from Phonotheque.accounts_app.forms import UserRegistrationForm
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

    def test_user_creation_form__with_valid_data__expect_user_creation(self):
        user_form = UserRegistrationForm(self.valid_user_data)
        self.assertTrue(user_form.is_valid())

    def test_user_creation_form__with_single_char_first_name__raises(self):
        user_form = UserRegistrationForm(self.valid_user_data.copy())
        # overwrite valid data field to check if validation fails
        user_form.data['first_name'] = 'a'

        # form fails
        self.assertFalse(user_form.is_valid())
        # won't be saved
        with self.assertRaises(Exception) as context:
            user_form.save()
        self.assertEqual("The User could not be created because the data didn't validate.", str(context.exception))
        # display message
        self.assertIn("Ensure this value has at least 2 characters (it has 1).", user_form.errors['first_name'])

    def test_user_creation_form__with_single_char_last_name__raises(self):
        user_form = UserRegistrationForm(self.valid_user_data.copy())
        # overwrite valid data field to check if validation fails
        user_form.data['last_name'] = 'a'

        # form fails
        self.assertFalse(user_form.is_valid())
        # won't be saved
        with self.assertRaises(Exception) as context:
            user_form.save()
        self.assertEqual("The User could not be created because the data didn't validate.", str(context.exception))
        # display message
        self.assertIn("Ensure this value has at least 2 characters (it has 1).", user_form.errors['last_name'])

    def test_user_creation_form__with_prohibited_chars_first_name__raises(self):
        user_form = UserRegistrationForm(self.valid_user_data.copy())
        invalid_names = ['123456', 'Ivan~', 'Pes#o', '@@', '\/+-', '==', '$%£', '\"\"']

        for invalid_first_name in invalid_names:
            user_form.data['first_name'] = invalid_first_name

            # form fails
            self.assertFalse(user_form.is_valid())
            # won't be saved
            with self.assertRaises(Exception) as context:
                user_form.save()
            self.assertEqual("The User could not be created because the data didn't validate.", str(context.exception))
            # display message
            self.assertIn("This name format won't work here, buddy.", user_form.errors['first_name'])

    def test_user_creation_form__with_prohibited_chars_last_name__raises(self):
        user_form = UserRegistrationForm(self.valid_user_data.copy())
        invalid_names = ['&*|?', 00, '32', 'x0x0', '****', "the_dude"]

        for invalid_last_name in invalid_names:
            user_form.data['last_name'] = invalid_last_name

            # form fails
            self.assertFalse(user_form.is_valid())
            # won't be saved
            with self.assertRaises(Exception) as context:
                user_form.save()
            self.assertEqual("The User could not be created because the data didn't validate.", str(context.exception))
            # display message
            self.assertIn("This name format won't work here, buddy.", user_form.errors['last_name'])

    def test_user_creation_form__with_blank_first_name__raises(self):
        user_form = UserRegistrationForm(self.valid_user_data.copy())
        # overwrite valid data field to check if validation fails
        user_form.data['last_name'] = ''

        # form fails
        self.assertFalse(user_form.is_valid())
        # won't be saved
        with self.assertRaises(Exception) as context:
            user_form.save()
        self.assertEqual("The User could not be created because the data didn't validate.", str(context.exception))
        # display message
        self.assertIn("This field is required.", user_form.errors['last_name'])

    def test_user_creation_form__with_non_matching_passwords__raises(self):
        user_form = UserRegistrationForm(self.valid_user_data.copy())
        # overwrite valid data field to check if validation fails
        user_form.data['password2'] = 'PutinIsAFuckingFascist'

        # form fails
        self.assertFalse(user_form.is_valid())
        # won't be saved
        with self.assertRaises(Exception) as context:
            user_form.save()
        self.assertEqual("The User could not be created because the data didn't validate.", str(context.exception))
        # display message
        self.assertIn("Passwords don\'t match.", user_form.errors['password2'])

    def test_form_field_formatting__expect_to_obtain_formatting_from_mixin(self):
        user_form = UserRegistrationForm(self.valid_user_data.copy())
        for k, v in user_form.fields.items():
            expected_format = 'form-control rounded'
            actual_format = v.widget.attrs['class']
            self.assertEqual(expected_format, actual_format)

            expected_placeholder = f"Enter {k.title().replace('_', ' ')}"
            actual_placeholder = v.widget.attrs['placeholder']
            self.assertEqual(expected_placeholder, actual_placeholder)
