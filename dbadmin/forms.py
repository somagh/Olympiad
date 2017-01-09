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
            choices=[(x['rname'], x['rname']) for x in run_query("select rname from feol", fetch=True)], label='رشته'
        )


class M1M2DateForm(forms.Form):

    rname = forms.CharField(widget=forms.HiddenInput())
    yr = forms.IntegerField(widget=forms.HiddenInput())
    m1_date = forms.CharField(label="تاریخ مرحله اول")

    def __init__(self, *args, **kwargs):
        rname = kwargs.pop('rname')
        yr = kwargs.pop('yr')
        super().__init__(*args, **kwargs)
        self.fields['rname'].initial = rname
        self.fields['yr'].initial = yr
        self.fields['m1_date'].initial = run_query('select edate from emtehan where eid='
                                                   '(select eid from m1 where yr=%s and rname=%s)',
                                                   [yr, rname], fetch=True)[0]['edate']
        m2days = run_query('select * from RE natural join emtehan where rname=%s and yr=%s', [rname, yr], fetch=True)
        for m2day in m2days:
            self.fields['m2_' + m2day['rnum'] + '_date'] = forms.CharField(initial=m2day['date'])
            self.fields['m2_' + m2day['rnum'] + '_darsad'] = forms.IntegerField(initial=m2day['darsad'])