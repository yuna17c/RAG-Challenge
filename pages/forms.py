from django import forms

class MyForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea)