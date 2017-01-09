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
            choices=[(x['fname'], x['fname']) for x in run_query("select fname from Field", fetch=True)], label='رشته'
        )


class M1M2DateForm(forms.Form):

    rname = forms.CharField(widget=forms.HiddenInput())
    yr = forms.IntegerField(widget=forms.HiddenInput())
    m2_day_count = forms.IntegerField(widget=forms.HiddenInput())
    m1_date = forms.CharField(label="تاریخ مرحله اول")

    def __init__(self, *args, **kwargs):
        rname = kwargs.pop('rname')
        yr = kwargs.pop('yr')
        super().__init__(*args, **kwargs)
        self.fields['rname'].initial = rname
        self.fields['yr'].initial = yr
        self.fields['m1_date'].initial = run_query('select edate from exam where eid='
                                                   '(select eid from m1 where year=%s and fname=%s)',
                                                   [yr, rname], fetch=True)[0]['edate']
        m2days = run_query('select * from examday natural join exam where fname=%s and year=%s', [rname, yr], fetch=True, raise_not_found=True)
        self.fields['m2_day_count'].initial = len(m2days)
        for m2day in m2days:
            self.fields['m2_' + str(m2day['num']) + '_date'] = forms.CharField(initial=m2day['edate'],label="تاریخ",required=False)
            self.fields['m2_' + str(m2day['num']) + '_darsad'] = forms.IntegerField(initial=m2day['percentage'],label="درصد تاثیر",required=False)

        class ProblemForm(forms.Form):
    score = forms.IntegerField(label='نمره')
    type = forms.BooleanField(label='تستی', required=False)
    text = forms.CharField(widget=forms.Textarea(), label='متن سوال')
    author = forms.CharField(initial='044013221')  # TODO: REMOVE THIS LATER

    def clean(self):
        data = super().clean()
        if 'type' in data and data['type'] == True:
            data['type'] = True
        else:
            data['type'] = False
        return data

    def __init__(self, **kwargs):
        eid = kwargs.pop('eid')
        pnum = kwargs.pop('pnum')
        super().__init__(**kwargs)
        if not eid or not pnum:
            return

        problem = run_query('select * from problem where eid=%s and pnum=%s',
                            [eid, pnum], fetch=True)[0]
        self.fields['score'].initial = problem['score']
        self.fields['type'].initial = problem['type']
        self.fields['text'].initial = problem['text']
        self.fields['author'].initial = problem['author_id']


class CourseForm(forms.Form):
    name = forms.CharField(label='نام')
    minpass = forms.CharField(label='حداقل درصد قبولی')
    teacher = forms.CharField(label='کد ملی مدرس')
    wage = forms.IntegerField(label='حقوق ساعتی استاد')

