from django.http.response import HttpResponse
from django.http import HttpResponse
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView, FormView
from rest_framework.response import Response
from rest_framework.views import APIView

from Olympiad.helpers import OlympiadMixin, run_query
from olympiad_manager.forms import ProblemForm, GradeForm, AddGraderForm


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




class GradeView(FormView):
    template_name = 'olympiad/grade.html'
    form_class = GradeForm

    def dispatch(self, request, *args, **kwargs):
        self.eid = self.kwargs['eid']
        self.user = request.session['user']
        exam = run_query('select fname, year from m1 where eid=%s', [self.eid], fetch=True,
                         raise_not_found=False)
        if len(exam) == 0:
            exam = run_query('select fname, year from examDay where eid=%s',
                             [self.eid], fetch=True, raise_not_found=False)
            if len(exam) == 0:
                exam = run_query('select fname, year from summercampexam where eid=%s',
                                 [self.eid], fetch=True, raise_not_found=False)[0]
                self.scholars = run_query(
                    'select national_code, name from m2_accepted join human on '
                    'scholar_id=national_code where fname=%s and year=%s',
                    [exam['fname'], exam['year']], fetch=True)
            else:
                exam = exam[0]
                self.scholars = run_query(
                    'select national_code, name from m1_accepted join human on '
                    'scholar_id=national_code where fname=%s and year=%s',
                    [exam['fname'], exam['year']], fetch=True)
        else:
            exam = exam[0]
            self.scholars = run_query('select national_code, name from participation natural join '
                                      'human where fname=%s and year=%s',
                                      [exam['fname'], exam['year']], fetch=True)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        for scholar in self.scholars:
            id = scholar['national_code']
            score = form.cleaned_data[id]
            if score == "":
                run_query('delete from grade where grader_id=%s and scholar_id=%s and eid=%s '
                          'and pnum=%s', [self.user['national_code'],
                                          id, self.eid, self.kwargs['pnum']])
            else:
                run_query('insert into grade(score, scholar_id, eid, pnum, grader_id) '
                          'values (%s, %s, %s, %s, %s) on conflict(scholar_id, eid, pnum, '
                          'grader_id) do update set score=%s',
                          [score, id, self.eid, self.kwargs['pnum'], self.user['national_code'],
                           score])
        return HttpResponse('ok')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['problem'] = run_query('select * from problem where eid=%s and pnum=%s',
                                       [self.eid, self.kwargs['pnum']], fetch=True)[0]
        context['scholars'] = self.scholars
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['eid'] = self.eid
        kwargs['pnum'] = self.kwargs['pnum']
        kwargs['scholars'] = self.scholars
        kwargs['grader_id'] = self.user['national_code']
        return kwargs
