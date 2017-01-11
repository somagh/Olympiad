from django.db import connection
from django.urls import reverse
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

from Olympiad.helpers import OlympiadMixin, run_query
from olympiad_manager.forms import SummerExamForm


class SummerExamListView(OlympiadMixin, TemplateView):
    template_name = 'olympiad/summer_exams.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['exams'] = run_query('select * from SummerCampExam natural join Exam '
                                     'where fname=%s and year=%s',
                                     [self.fname, self.year], fetch=True, raise_not_found=False)
        return context


class AddSummerExamView(OlympiadMixin, FormView):
    template_name = 'olympiad/summer_exam.html'
    form_class = SummerExamForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['fname'] = self.fname
        kwargs['year'] = self.year
        return kwargs

    def get_success_url(self):
        return reverse('olympiad:summer-camp-exam:list', args=[self.fname, self.year])

    def form_valid(self, form):
        data = form.cleaned_data
        cursor = connection.cursor()
        cursor.execute('insert into exam(edate) values(%s) returning eid', [data['date']])
        eid = cursor.fetchone()[0]
        run_query('insert into SummerCampExam(fname, year, cname, name, eid, percentage) '
                  'values(%s, %s, %s, %s, %s, %s)',
                  [self.fname, self.year, data['course'], data['name'], eid, data['percentage']])
        return super().form_valid(form)


class EditSummerExamView(OlympiadMixin, FormView):
    template_name = 'olympiad/summer_exam.html'
    form_class = SummerExamForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['fname'] = self.fname
        kwargs['year'] = self.year
        kwargs['eid'] = self.kwargs['eid']
        return kwargs

    def get_success_url(self):
        return reverse('olympiad:summer-camp-exam:list', args=[self.fname, self.year])

    def form_valid(self, form):
        data = form.cleaned_data
        run_query('update exam set edate=%s where eid=%s', [data['date'], self.kwargs['eid']])
        run_query('update SummerCampExam set name=%s, cname=%s, percentage=%s where eid=%s',
                  [data['name'], data['course'], data['percentage'], self.kwargs['eid']])
        return super().form_valid(form)