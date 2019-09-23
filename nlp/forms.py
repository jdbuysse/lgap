from django import forms
from django.core.exceptions import ValidationError
# for translation, prob don't need
from django.utils.translation import ugettext_lazy as _
from .models import Text

# TextForm is a custom class not some django thing fyi
# this is the 'form and function view' version that doesn't do database stuff or model forms
class TextForm(forms.Form):

    a = forms.CharField(label='', widget=forms.TextInput(attrs={'size': '40'}))

# this is the ModelForms version where you use the model as a template via Meta:
class AddText(forms.ModelForm):

    class Meta:
        model = Text
        fields = ('title',)



# class NewTextForm(forms.Form):
#
#     text = forms.CharField(label='', widget=forms.TextInput(attrs={'size': '40'}))
#
#     def add_new_text(self):
#         data = self.cleaned_data['text']
#         # you'll put any text validation things here
#
#         return data


