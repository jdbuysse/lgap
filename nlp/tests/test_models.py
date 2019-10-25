
from django.test import TestCase, Client

from nlp.models import UploadText
from django.contrib.auth.models import User


class UploadTextModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.client = Client(HTTP_HOST='localhost:8000')
        # set up objects to be used by all test methods
        cls.user = User.objects.create_user(username='tammytestcase', password='1234')
        login = cls.client.login(username='tammytestcase', password='1234')
        UploadText.objects.create(
            id='3e510643-8545-4b42-9d09-ade16edc137a',
            owner=cls.user, title='test model title', description='for unit tests',
            fulltext='creating a test model',
        )

    def test_id_label(self):
        # uploadtext = UploadText.objects.get(id='3e510643-8545-4b42-9d09-ade16edc137a')
        # this grabs tammy testcase
        uploadtext = UploadText.objects.get(owner=1)
        field_label = uploadtext._meta.get_field('id').verbose_name
        self.assertEquals(field_label, 'id')

    


