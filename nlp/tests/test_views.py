from django.test import TestCase, Client
from django.urls import resolve


from nlp.views import index
from nlp.models import UploadText, User


# test out base.html elements on the home page
class BaseTemplateTest(TestCase):

    def test_base_appears_different_places(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'nlp/index.html', 'nlp/base.html')
        response = self.client.get('/post/new/')
        self.assertTemplateUsed(response, 'nlp/text_edit.html', 'nlp/base.html')


# home/landing page
class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, index)

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'nlp/index.html', 'nlp/base.html')


class TextsByUserListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        number_of_texts = 13
        cls.client = Client(HTTP_HOST='localhost:8000')
        # set up objects to be used by all test methods
        cls.user = User.objects.create_user(username='tammytestcase', password='1234')
        cls.user.save()
        login = cls.client.login(username='tammytestcase', password='1234')
        for i in range(number_of_texts):
            UploadText.objects.create(
                id=None, # in order to populate this I would need a unique ID for each
                owner=cls.user,
                title='test',
                description='testy',
                fulltext='testcase'
            )

    def test_view_url_exists_at_desired_loaction(self):
        login = self.client.login(username='tammytestcase', password='1234')
        response = self.client.get('nlp/mytexts')
        # fails because we are not logged in (see moz tutorial to implement)
        self.assertEqual(response.status_code, 200)

    def test_redirect_if_not_logged_in(self):
        # I don't have this implemented yet
        self.assertEqual(1, 1)


