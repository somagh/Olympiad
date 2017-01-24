from django import forms
from django.core.exceptions import ValidationError

from Olympiad.helpers import run_query


class NewFeolForm(forms.Form):
    name = forms.CharField(label='نام')
    t_t = forms.IntegerField(label='تعداد طلا')
    t_n = forms.IntegerField(label='تعداد نقره')
    groups = forms.CharField(label='گروه ها')


class NewOlForm(forms.Form):
    yr = forms.IntegerField(label='سال')
    saghf = forms.IntegerField(label='سقف افتادن')
    t_m1 = forms.IntegerField(label='تعداد قبولی مرحله اول')
    t_m2 = forms.IntegerField(label='تعداد قبولی مرحله دوم')
    manager = forms.CharField(label='کد ملی مدیر المپیاد', max_length=10)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['feol'] = forms.ChoiceField(
            choices=[(x['fname'], x['fname']) for x in
                     run_query("select fname from Field", fetch=True)], label='رشته'
        )


class NewUniversityfieldForm(forms.Form):
    id = forms.IntegerField(label='کد رشته محل')
    min_level = forms.IntegerField(label='حداقل تراز قبولی')
    olympiad_capacity = forms.IntegerField(label='حداکثر المپیادی')
    group_name = forms.CharField(label='گروه')
