from django import test as django_test

from Phonotheque.main_app.forms import CommentForm


class CommentFormTest(django_test.TestCase):
    VALID_COMMENT = {'body': '12CHARACTERS'}
    INVALID_COMMENT = {'body': '12CHARACTERS' * 60}
    EMPTY_COMMENT = {'body': ""}

    def test_comment_form__with_below_max_chars__expect_valid_(self):
        comment_form = CommentForm(self.VALID_COMMENT)
        self.assertTrue(comment_form.is_valid())

        for k, v in comment_form.fields.items():
            expected_format = 'form-control rounded-0'
            actual_format = v.widget.attrs['class']
            self.assertEqual(expected_format, actual_format)

            expected_placeholder = "Share your thoughts if you have any"
            actual_placeholder = v.widget.attrs['placeholder']
            self.assertEqual(expected_placeholder, actual_placeholder)

            expected_rows = 8
            actual_rows = v.widget.attrs['rows']
            self.assertEqual(expected_rows, actual_rows)

    def test_comment_form__with_over_max_chars__expect_invalid_(self):
        comment_form = CommentForm(self.INVALID_COMMENT)
        self.assertFalse(comment_form.is_valid())

        comment_form = CommentForm(self.EMPTY_COMMENT)
        self.assertFalse(comment_form.is_valid())
