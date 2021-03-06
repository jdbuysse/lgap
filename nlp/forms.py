from django import forms
from django.core.exceptions import ValidationError
# for translation, prob don't need
from django.utils.translation import ugettext_lazy as _
from .models import UploadText


# this is the modelform version where you base the form off an existing model
class UploadForm(forms.ModelForm):

    class Meta:
        model = UploadText
        fields = ('title', 'description', 'fulltext',)

# add this another time. you'll want to use django's validators.py to write a custom validator
# see: https://stackoverflow.com/questions/3648421/only-accept-a-certain-file-type-in-filefield-server-side
# note this could also be a good solution for query string validation (could also use a hash table to validate there)
# class UploadFileForm(forms.ModelForm):
#
#     class Meta:
#         model = UploadText
#         title = forms.CharField(max_length=50)
#         file = forms.FileField()


# form to select a text and process it. for user does this once per session or per new text.
class ProcessTextForm(forms.Form):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user') # to get request.user
        super(ProcessTextForm, self).__init__(*args, **kwargs)
        # create a list of objects rather than using a queryset
        self.fields['text'].queryset = UploadText.objects.filter(owner=user)

    text = forms.ModelChoiceField(queryset=None, widget=forms.Select, required=True)


class WorkspaceForm(forms.Form):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(WorkspaceForm, self).__init__(*args, **kwargs)
        self.fields['text'].queryset = UploadText.objects.filter(owner=user)

    #text = forms.ModelChoiceField(queryset=UploadText.objects.all())
    text = forms.ModelChoiceField(queryset=None, widget=forms.Select, required=True)
    query = forms.CharField(label='', widget=forms.TextInput(attrs={'size': '40'}))


# this is the 'form and function view' version that doesn't do database stuff or model forms.
# this is used for the sentence parsing cause that doesn't have to interact with DB
class TextForm(forms.Form):
    a = forms.CharField(label='', widget=forms.TextInput(attrs={'size': '40'}))


