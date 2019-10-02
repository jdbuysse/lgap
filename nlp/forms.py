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


# TextForm is a custom class not some django thing fyi
# this is the 'form and function view' version that doesn't do database stuff or model forms.
# this is used for the sentence parsing cause that doesn't have to interact with DB
class TextForm(forms.Form):

    a = forms.CharField(label='', widget=forms.TextInput(attrs={'size': '40'}))

