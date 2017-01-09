from django.views.generic import FormView, TemplateView

from Olympiad.helpers import run_query, OlympiadMixin
from olympiad_manager.forms import M1M2DateForm, ProblemForm, CourseForm


class OlympiadView(OlympiadMixin, TemplateView):
    template_name = 'olympiad/olympiad.html'


class M1M2Date(OlympiadMixin, FormView):
    template_name = 'olympiad/m1m2date.html'
    form_class = M1M2DateForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['rname'] = self.fname
        kwargs['yr'] = self.year
        return kwargs

    def form_valid(self, form):
        run_query(
            "update exam set edate=%s where eid=(select eid from m1 where fname=%s and year=%s)",
            [form.data['m1_date'], form.data['rname'], form.data['yr']])
        old_count = \
            run_query("select count(*) from examday natural join m2 where fname=%s and year=%s",
                      [form.data['rname'], form.data['yr']], fetch=True)[0]['count']
        counter = 0
        for i in range(int(form.data['m2_day_count'])):
            print(i)
            print(counter)
            if form.data['m2_' + str(i) + '_date'] == "":
                continue
            if counter < old_count:
                run_query(
                    "update examday set percentage=%s where fname=%s and year=%s and num=%s",
                    [form.data['m2_' + str(i) + '_darsad'], form.data['rname'], form.data['yr'],
                     counter])
            else:
                run_query(
                    "insert into examday(fname,year,num,percentage) values(%s,%s,%s,%s)",
                    [form.data['rname'], form.data['yr'], counter,
                     form.data['m2_' + str(i) + '_darsad']])
            run_query(
                "update exam set edate=%s where eid=(select eid from examday where fname=%s and year=%s and num=%s)",
                [form.data['m2_' + str(i) + '_date'], form.data['rname'], form.data['yr'], counter])
            counter += 1
        for i in range(counter, old_count):
            run_query(
                "delete from exam where eid=(select eid from examday where fname=%s and year=%s and num=%s)",
                [form.data['rname'], form.data['yr'], i])
        return super().form_valid(form)


class AddProblemView(OlympiadMixin, FormView):
    template_name = 'olympiad/problem.html'
    form_class = ProblemForm

    def form_valid(self, form):
        data = form.cleaned_data
        run_query(
            'insert into problem(eid, type, score, text, author_id) values(%s, %s, %s, %s, %s)',
            [self.kwargs['eid'], data['type'], data['score'], data['text'], data['author']])
        return super().form_valid(form)


class EditProblemView(OlympiadMixin, FormView):
    template_name = 'olympiad/problem.html'
    form_class = ProblemForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['eid'] = self.kwargs['eid']
        kwargs['pnum'] = self.kwargs['pnum']
        return kwargs

    def form_valid(self, form):
        data = form.cleaned_data
        run_query('update problem set type=%s, score=%s, text=%s, author_id=%s'
                  'where eid=%s and pnum=%s',
                  [data['type'], data['score'], data['text'], data['author'], self.kwargs['eid'],
                   self.kwargs['pnum']])
        return super().form_valid(form)


class ProblemListView(OlympiadMixin,TemplateView):
    template_name='olympiad/problems.html'

    def get_context_data(self, **kwargs):
        super()
        kwargs['problems']=run_query('select * from problem join human on '
                                     'problem.author_id=human.national_code '
                                     'where eid=%s order by pnum',[kwargs['eid']],
                                     fetch=True, raise_not_found=False)
        return kwargs


class AddCourseView(OlympiadMixin, FormView):
    template_name = 'olympiad/course.html'
    form_class = CourseForm

    def form_valid(self, form):
        data = form.cleaned_data
        run_query('insert into course(fname, year, cname, minpass, teacher_id, hourly_wage) '
                  'values(%s, %s, %s, %s, %s, %s)',
                  [self.fname, self.year, data['name'], data['minpass'],
                   data['teacher'], data['wage']])
        return super().form_valid(form)


class EditCourseView(OlympiadMixin, FormView):
    template_name = 'olympiad/course.html'
    form_class = CourseForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['fname'] = self.fname
        kwargs['year'] = self.year
        self.cname = self.kwargs['cname'].replace('-', ' ')
        kwargs['cname'] = self.cname
        return kwargs

    def form_valid(self, form):
        data = form.cleaned_data
        run_query('update course set cname=%s, minpass=%s, teacher_id=%s, hourly_wage=%s',
                  [data['name'], data['minpass'], data['teacher'], data['wage']])
        return super().form_valid(form)

class CourseListView(OlympiadMixin,TemplateView):
    template_name='olympiad/courses.html'
    def get_context_data(self, **kwargs):
        super()
        kwargs['courses']=run_query('select * from course where fname=%s and year=%s' ,[self.fname,self.year],fetch=True,raise_not_found=False)
        return kwargs

