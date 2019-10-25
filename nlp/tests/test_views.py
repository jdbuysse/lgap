from django.test import TestCase
from django.urls import resolve


from nlp.views import index


# test out base.html elements on the home page
class BaseTemplateTest(TestCase):

    def test_base_appears_at_home(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'nlp/index.html', 'nlp/base.html')

    

class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, index)

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'nlp/index.html', 'nlp/base.html')


