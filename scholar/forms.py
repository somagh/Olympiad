from django import forms
from django.core.exceptions import ValidationError

from Olympiad.helpers import run_query


class RegisterOlympiadForm(forms.Form):
    fname = forms.CharField(widget=forms.HiddenInput)
    year = forms.IntegerField(widget=forms.HiddenInput)


class RequestUniversityFieldForm(forms.Form):
    field = forms.ChoiceField(label='رشته مورد علاقه')

    def __init__(self, groups, initial=None, **kwargs):
        super().__init__(**kwargs)
        fields = []
        for group in groups:
            fields += run_query('select * from UniversityField where gp_name=%s',
                                [group['gp_name']], fetch=True,
                                raise_not_found=False)
        self.fields['field'].choices = [(field['id'], field['name']) for field in fields]
        if initial:
            self.fields['field'].initial = initial

    def clean(self):
        super().clean()
        if not self.data['field'] in [str(choice[0]) for choice in self.fields['field'].choices]:
            raise ValidationError('شما اجازه ثبت نام درین رشته را ندارید')
