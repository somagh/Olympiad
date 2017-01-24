from django import forms
from django.http.response import Http404

from Olympiad.helpers import run_query


class M1M2DateForm(forms.Form):
    rname = forms.CharField(widget=forms.HiddenInput())
    yr = forms.IntegerField(widget=forms.HiddenInput())
    m2_day_count = forms.IntegerField(widget=forms.HiddenInput())
    m1_date = forms.CharField(label="تاریخ")
    m1_eid=forms.IntegerField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        rname = kwargs.pop('rname')
        yr = kwargs.pop('yr')
        super().__init__(*args, **kwargs)
        self.fields['rname'].initial = rname
        self.fields['yr'].initial = yr
        self.fields['m1_date'].initial = run_query('select edate from exam where eid='
                                                   '(select eid from m1 where year=%s and fname=%s)',
                                                   [yr, rname], fetch=True, raise_not_found=False)[0]['edate']
        self.fields['m1_eid'].initial = run_query('select eid from exam where eid='
                                                   '(select eid from m1 where year=%s and fname=%s)',
                                                   [yr, rname], fetch=True, raise_not_found=False)[0]['eid']
        m2days = run_query('select * from examday natural join exam where fname=%s and year=%s', [rname, yr], fetch=True, raise_not_found=False)
        self.fields['m2_day_count'].initial = len(m2days)
        for m2day in m2days:
            self.fields['m2_' + str(m2day['num']) + '_date'] = forms.CharField(initial=m2day['edate'],label="تاریخ",required=False)
            self.fields['m2_' + str(m2day['num']) + '_darsad'] = forms.IntegerField(initial=m2day['percentage'],label="درصد تاثیر",required=False)
            self.fields['m2_'+str(m2day['num'])+'_eid']=forms.IntegerField(widget=forms.HiddenInput(),initial=m2day['eid'])


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

    def __init__(self, eid=None, pnum=None, **kwargs):
        super().__init__(**kwargs)
        if eid is not None:
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

    def __init__(self, course=None, **kwargs):
        super().__init__(**kwargs)
        if course:
            self.fields['name'].initial = course['cname']
            self.fields['minpass'].initial = course['minpass']
            self.fields['teacher'].initial = course['teacher_id']
            self.fields['wage'].initial = course['hourly_wage']


class SummerExamForm(forms.Form):
    name = forms.CharField(label='نام آزمون')
    percentage = forms.IntegerField(label='درصد تاثیر')
    course = forms.ChoiceField(label='مربوط به درس', required=False, help_text='اگر این امتحان مربوط به درس خاصی '
                               'است، درس مربوطه را انتخاب کنید')
    date = forms.CharField(label='تاریخ برگزاری')

    def __init__(self, fname=None, year=None, eid=None, **kwargs):
        super().__init__(**kwargs)
        self.fields['course'].choices = [(None, '----')] + [
            (c['cname'], c['cname']) for c in run_query('select cname from course '
                                                        'where fname=%s and year=%s',
                               [fname, year], fetch=True, raise_not_found=False)
        ]

        if eid:
            exam = run_query('select * from SummerCampExam natural join Exam where eid=%s', [eid],
                             fetch=True)[0]
            self.fields['name'].initial = exam['name']
            self.fields['percentage'].initial = exam['percentage']
            self.fields['course'].initial = exam['cname'] if exam['cname'] is not None else '----'
            self.fields['date'].initial = exam['edate']

    def clean(self):
        data = super().clean()
        if not data['course']:
            data['course'] = None
        return data

class AddGraderForm(forms.Form):
    pass


class GradeForm(forms.Form):

    def __init__(self, eid, pnum, scholars, grader_id, **kwargs):
        super().__init__(**kwargs)
        for i, scholar in enumerate(scholars):
            self.fields[scholar['national_code']] = forms.CharField(label=scholar['name'],
                                                                    required=False)
            try:
                grade = run_query('select score from grade where '
                                  'scholar_id=%s and eid=%s and grader_id=%s '
                                  'and pnum=%s', [scholar['national_code'], eid, grader_id, pnum],
                                  fetch=True)[0]
                self.fields[scholar['national_code']].initial = grade['score']
            except Http404:
                pass

class LevelForm(forms.Form):
    def __init__(self,year,fname,medalists,**kwargs):
        super().__init__(**kwargs)
        for i,medalist in enumerate(medalists):
            self.fields[medalist['scholar_id']]=forms.IntegerField(label=medalist['name'],
                                                                    required=False)
            try:
                level = run_query('select level from scholar where id=%s',[medalist['scholar_id']],fetch=True)[0]
                self.fields[medalist['scholar_id']].initial = level['level']
            except Http404:
                pass

