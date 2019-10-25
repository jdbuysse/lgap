from django.test import TestCase

from nlp.forms import TextForm

# UploadForm has it's components tested in the model tests, I think, so should already be covered there


# I went in circles trying to figure this out. not sure why it isn't working. come back to this later?
# do I need to go the route of @classmethod? the django tutorial doesn't but I don't see how else
# might need to go back to testing book for this
# class TextForm(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         cls.form = TextForm({'': 'hi'})
#
#     def test_textform(self):
#         testtext = TextForm.objects.get(1)
#         print(testtext)
#         # I guess I want to push data into the form? I don't see how to test this usefully
#         self.assertTrue(testtext.is_valid())



