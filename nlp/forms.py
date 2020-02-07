from django import forms
from django.core.exceptions import ValidationError
# for translation, prob don't need
from django.utils.translation import ugettext_lazy as _
from .models import UploadText, Document, ByteText, Book


# this is the modelform version where you base the form off an existing model
class UploadForm(forms.ModelForm):

    class Meta:
        model = UploadText
        fields = ('title', 'description', 'fulltext',)


# form to select a text and process it. for user does this once per session or per new text.
class ProcessTextForm(forms.Form):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user') # to get request.user
        super(ProcessTextForm, self).__init__(*args, **kwargs)
        # create a list of objects rather than using a queryset
        self.fields['text'].queryset = UploadText.objects.filter(owner=user)

    text = forms.ModelChoiceField(queryset=None, widget=forms.Select, required=True)



class WorkspaceForm(forms.Form):

    # for now this is all texts, not user-specific. fix later.
    text = forms.ModelChoiceField(queryset=UploadText.objects.all())
    query = forms.CharField(label='', widget=forms.TextInput(attrs={'size': '40'}))


# this is the 'form and function view' version that doesn't do database stuff or model forms.
# this is used for the sentence parsing cause that doesn't have to interact with DB
class TextForm(forms.Form):
    a = forms.CharField(label='', widget=forms.TextInput(attrs={'size': '40'}))


# dry run for file manipulation
class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('description', 'document', )


# form to go directly from upload to bytes
class UploadToBytesForm(forms.ModelForm):

    class Meta:
        model = ByteText
        fields = ('title', 'bytefile')

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ('title', 'author', 'pdf')
