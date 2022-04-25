from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class ProfilesListViewTests(TestCase):
    def test_get__expect_correct_template(self):
        response = self.client.get(reverse('index_page'))

        self.assertTemplateUsed(response, 'main_app/index.html')
