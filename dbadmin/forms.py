from django import forms

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['feol'] = forms.ChoiceField(
            choices=[(x[0], x[0]) for x in run_query("select rname from feol", fetch=True)], label='رشته'
        )

