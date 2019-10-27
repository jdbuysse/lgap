
from django.test import TestCase, Client

from nlp.models import UploadText
from django.contrib.auth.models import User


# These don't seem all that useful. proof of concept at least.
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

    # the following check that the values of the field labels (verbose_name) are alright
    def test_id_label(self):
        # this grabs tammy testcase
        uploadtext = UploadText.objects.get(owner=1)
        field_label = uploadtext._meta.get_field('id').verbose_name
        self.assertEquals(field_label, 'id')

    def test_owner_label(self):
        uploadtext = UploadText.objects.get(owner=1)
        field_label = uploadtext._meta.get_field('owner').verbose_name
        self.assertEquals(field_label, 'owner')

    def test_title_label(self):
        uploadtext = UploadText.objects.get(owner=1)
        field_label = uploadtext._meta.get_field('title').verbose_name
        self.assertEquals(field_label, 'title')

    def test_description_label(self):
        uploadtext = UploadText.objects.get(owner=1)
        field_label = uploadtext._meta.get_field('description').verbose_name
        self.assertEquals(field_label, 'description')

    def test_fulltext_label(self):
        uploadtext = UploadText.objects.get(owner=1)
        field_label = uploadtext._meta.get_field('fulltext').verbose_name
        self.assertEquals(field_label, 'fulltext')

    # tests for length specifications, to make sure those are correctly defined in model
    def test_title_max_length(self):
        uploadtext = UploadText.objects.get(owner=1)
        max_length = uploadtext._meta.get_field('title').max_length
        self.assertEquals(max_length, 40)

    def test_description_max_length(self):
        uploadtext = UploadText.objects.get(owner=1)
        max_length = uploadtext._meta.get_field('description').max_length
        self.assertEquals(max_length, 240)

    def test_fulltext_max_length(self):
        uploadtext = UploadText.objects.get(owner=1)
        max_length = uploadtext._meta.get_field('fulltext').max_length
        self.assertEquals(max_length, 100000)

    # make sure the model display follows the right formatting
    def test_object_name(self):
        uploadtext = UploadText.objects.get(owner=1)
        expected_object_name = f'{uploadtext.id} ({uploadtext.title})'
        self.assertEquals(expected_object_name, str(uploadtext))
