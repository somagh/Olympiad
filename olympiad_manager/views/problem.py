from django.urls import reverse
from django.views.generic import TemplateView, FormView

from Olympiad.helpers import OlympiadMixin, run_query
from olympiad_manager.forms import ProblemForm


class ProblemListView(OlympiadMixin, TemplateView):
    template_name = 'olympiad/problems.html'

    def get_context_data(self, **kwargs):
        super()
        kwargs['problems'] = run_query('select * from problem join human on '
                                       'problem.author_id=human.national_code '
                                       'where eid=%s order by pnum', [kwargs['eid']],
                                       fetch=True, raise_not_found=False)
        is_summer_exam = run_query('select count(*) from summercampexam where eid=%s',
                                   [kwargs['eid']], fetch=True)[0]
        if is_summer_exam['count'] > 0:
            kwargs['back_url'] = reverse('olympiad:summer-camp-exam:list', args=[self.fname,
                                                                                 self.year])
        else:
            kwargs['back_url'] = reverse('olympiad:m1m2date', args=[self.fname, self.year])
        return kwargs


class AddProblemView(OlympiadMixin, FormView):
    template_name = 'olympiad/problem.html'
    form_class = ProblemForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['eid'] = self.kwargs['eid']
        return context

    def get_success_url(self):
        return reverse('olympiad:problem:list', args=[self.fname, self.year, self.kwargs['eid']])

    def form_valid(self, form):
        data = form.cleaned_data
        run_query(
            'insert into problem(eid, type, score, text, author_id) values(%s, %s, %s, %s, %s)',
            [self.kwargs['eid'], data['type'], data['score'], data['text'], data['author']])
        return super().form_valid(form)


class EditProblemView(OlympiadMixin, FormView):
    template_name = 'olympiad/problem.html'
    form_class = ProblemForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['eid'] = self.kwargs['eid']
        return context

    def get_success_url(self):
        return reverse('olympiad:problem:list', args=[self.fname, self.year, self.kwargs['eid']])

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
