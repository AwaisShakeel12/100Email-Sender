from django import forms

class NumberForm(forms.Form):
    n = forms.CharField(label='Number of Emails', widget=forms.TextInput(attrs={'class': 'form-control form-input'}))

