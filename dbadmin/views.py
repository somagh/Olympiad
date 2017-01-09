from django.db import connection
from django.db.models import QuerySet
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.generic import FormView
from django.views.generic import TemplateView

from Olympiad.helpers import run_query, OlympiadMixin
from dbadmin.forms import NewFeolForm, NewOlForm, M1M2DateForm, ProblemForm, CourseForm


class newFeol(FormView):
    template_name = 'dbadmin/newFeol.html'
    form_class = NewFeolForm

    def form_valid(self, form):
        run_query("insert into field(fname, gold_no, silver_no) values(%s,%s,%s)",
                  [form.data['name'], form.data['t_t'],
                   form.data['t_n']])
        groups = form.data['groups'].split('-')
        for group in groups:
            run_query("insert into groups(fname, gp_name) values(%s, %s)",
                      [form.data['name'], group])
        return HttpResponse("رشته جدید با موفقیت اضافه شد")


class NewOl(FormView):
    form_class = NewOlForm
    template_name = 'dbadmin/newOl.html'

    def form_valid(self, form):
        run_query(
            "insert into olympiad(fname, max_fail, year, m1_no, m2_no) values(%s,%s,%s,%s,%s)",
            [form.data['feol'], form.data['saghf'], form.data['yr'], form.data['t_m1'],
             form.data['t_m2']])
        return HttpResponse("المپیاد جدید با موفقیت اضافه شد")


class OlympiadView(OlympiadMixin, TemplateView):
    template_name = 'dbadmin/olympiad.html'


class M1M2Date(OlympiadMixin, FormView):
    template_name = 'dbadmin/m1m2date.html'
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
    template_name = 'dbadmin/problem.html'
    form_class = ProblemForm

    def form_valid(self, form):
        data = form.cleaned_data
        run_query(
            'insert into problem(eid, type, score, text, author_id) values(%s, %s, %s, %s, %s)',
            [self.kwargs['eid'], data['type'], data['score'], data['text'], data['author']])
        return super().form_valid(form)


class EditProblemView(OlympiadMixin, FormView):
    template_name = 'dbadmin/problem.html'
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


class AddCourseView(OlympiadMixin, FormView):
    template_name = 'dbadmin/course.html'
    form_class = CourseForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        self.fname = self.kwargs['fname'].replace('-', ' ')
        self.year = self.kwargs['year']
        kwargs['fname'] = self.fname
        kwargs['year'] = self.year
        return kwargs

    def form_valid(self, form):
        data = form.cleaned_data
        run_query('insert into course(fname, year, cname, minpass, teacher_id, hourly_wage) '
                  'values(%s, %s, %s, %s, %s, %s)',
                  [self.fname, self.year, data['cname'], data['minpass'],
                   data['teacher_id'], data['hourly_wage']])
        return super().form_valid(form)


class EditCourseView(OlympiadMixin, FormView):
    pass
