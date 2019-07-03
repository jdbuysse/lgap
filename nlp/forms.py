from django import forms


class TextForm(forms.Form):

    a = forms.CharField(label='', widget=forms.TextInput(attrs={'size': '40'}))

