from django.http import HttpResponse
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView, FormView
from rest_framework.response import Response
from rest_framework.views import APIView

from Olympiad.helpers import OlympiadMixin, run_query
from olympiad_manager.forms import ProblemForm, AddGraderForm


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
        context['title'] = 'اضافه کردن سوال'
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
        context['title'] = 'ویرایش سوال'
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

class ManageGraderView(OlympiadMixin,FormView):
    template_name='olympiad/manage-graders.html'
    form_class = AddGraderForm

    def dispatch(self, request, *args, **kwargs):
        self.eid = kwargs['eid']
        self.pnum = kwargs['pnum']
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('olympiad:problem:graders', args=[self.fname, self.year,self.eid,self.pnum])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['graders'] = run_query("select * from grading join human on grader_id=national_code where eid=%s and pnum=%s",[self.eid,self.pnum],fetch=True,raise_not_found=False)
        context['eid']=self.eid
        context['pnum']=self.pnum
        return context

    def form_valid(self,form):
        data=form.data
        for i in range(int(data['new_grader_count'])):
            if form.data['new_code_' + str(i)] == "":
                continue
            run_query('insert into grading(grader_id,eid,pnum) values(%s,%s,%s)',[form.data['new_code_' + str(i)],self.eid,self.pnum])
        return super().form_valid(form)

class DeleteGraderView(APIView):
    def post(self,request,*args,**kwargs):
        run_query('delete from grading where eid=%s and pnum=%s and grader_id=%s',[request.POST.get('eid'),request.POST.get('pnum'),request.POST.get('national_code')])
        return Response()


