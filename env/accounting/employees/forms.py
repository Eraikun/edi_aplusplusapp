from django import forms

class NameForm(forms.Form):
    searchTerm = forms.CharField(label='employee\'s name')