from django import forms

from Olympiad.helpers import run_query


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
                                                   [yr, rname], fetch=True, raise_not_found=False)[0]['edate']
        m2days = run_query('select * from examday natural join exam where fname=%s and year=%s', [rname, yr], fetch=True, raise_not_found=False)
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
        if 'eid' in kwargs and 'pnum' in kwargs:
            eid = kwargs.pop('eid')
            pnum = kwargs.pop('pnum')
        else:
            super().__init__(**kwargs)
            return

        super().__init__(**kwargs)

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

    def __init__(self, **kwargs):
        if 'cname' in kwargs:
            fname = kwargs.pop('fname')
            year = kwargs.pop('year')
            cname = kwargs.pop('cname')
            super().__init__(**kwargs)
            course = run_query('select * from course where fname=%s and year=%s and cname=%s',
                               [fname, year, cname], fetch=True)[0]
            self.fields['name'].initial = course['cname']
            self.fields['minpass'].initial = course['minpass']
            self.fields['teacher'].initial = course['teacher_id']
            self.fields['wage'].initial = course['hourly_wage']
        else:
            super().__init__(**kwargs)