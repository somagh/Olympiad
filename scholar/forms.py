from django import forms

class RegisterOlympiadForm(forms.Form):
    fname=forms.CharField(widget=forms.HiddenInput)
    year=forms.IntegerField(widget=forms.HiddenInput)