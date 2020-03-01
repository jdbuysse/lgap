from django.test import TestCase

from nlp.forms import TextForm

# UploadForm is a modelform so it should have its components already tested in models


# This wasn't working before because I called it TextForm instead TextFormTest
class TextFormTest(TestCase):

    def test_textform_field_label(self):
        form = TextForm()
        self.assertTrue(form.fields['a'].label == '')

    def test_textform_max_length(self):
        form = TextForm()
        self.assertEquals(form.fields['a'].max_length, None)



# any reason to mess around with @classmethod?
#
# class TextFormTest(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         cls.form = TextForm({'': 'hi'})
#
#     def test_textform(self):
#         testtext = TextForm.objects.get(1)
#         print(testtext)
#         # I guess I want to push data into the form? I don't see how to test this usefully
#         self.assertTrue(testtext.is_valid())



