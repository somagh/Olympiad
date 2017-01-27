from django.urls import reverse
from django.views.generic import FormView, TemplateView

from Olympiad.helpers import OlympiadMixin, run_query
from olympiad_manager.forms import CourseForm, TeachingHourForm


class CourseListView(OlympiadMixin, TemplateView):
    template_name = 'olympiad/courses.html'

    def get_context_data(self, **kwargs):
        super()
        kwargs['courses'] = run_query('select * from course join human on teacher_id=national_code '
                                      'where fname=%s and year=%s '
                                      'order by cname',
                                      [self.fname, self.year], fetch=True, raise_not_found=False)
        return kwargs


class AddCourseView(OlympiadMixin, FormView):
    template_name = 'olympiad/course.html'
    form_class = CourseForm

    def get_success_url(self):
        return reverse('olympiad:course:list', args=[self.fname, self.year])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'اضافه کردن کلاس'
        return context

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
        self.course = run_query('select * from course where fname=%s and year=%s and cname=%s',
                                [self.fname, self.year, self.kwargs['cname']], fetch=True)[0]
        kwargs['course'] = self.course
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'ویرایش کلاس'
        return context

    def get_success_url(self):
        return reverse('olympiad:course:list', args=[self.fname, self.year])

    def form_valid(self, form):
        data = form.cleaned_data
        run_query('update course set cname=%s, minpass=%s, teacher_id=%s, hourly_wage=%s '
                  'where fname=%s and year=%s and cname=%s',
                  [data['name'], data['minpass'], data['teacher'], data['wage'], self.fname,
                   self.year, self.course['cname']])
        return super().form_valid(form)


class TeachingHourListView(TemplateView):
    template_name = 'olympiad/teaching-hours.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        run_query('select * from course where fname=%s and year=%s and cname=%s and teacher_id=%s ',
                  [kwargs['fname'], kwargs['year'], kwargs['cname'],
                   self.request.session['user']['national_code']], fetch=True)
        context['hours'] = run_query(
            "select st,en,day,en-st as time,(en-st)*hourly_wage as wage from teachinghour natural join course where cname=%s and fname=%s and year=%s",
            [kwargs['cname'], kwargs['fname'], kwargs['year']], fetch=True, raise_not_found=False)
        context['hourly_wage'] = \
        run_query("select hourly_wage from course where cname=%s and fname=%s and year=%s",
                  [kwargs['cname'], kwargs['fname'], kwargs['year']], fetch=True)[0]['hourly_wage']
        context['total_time'] = run_query(
            "select sum(en-st) as sum from teachinghour where cname=%s and fname=%s and year=%s",
            [kwargs['cname'], kwargs['fname'], kwargs['year']], fetch=True)[0]['sum']
        context['total_wage'] = run_query(
            "select sum((en-st)*hourly_wage) as total from course natural join teachinghour where cname=%s and fname=%s and year=%s",
            [kwargs['cname'], kwargs['fname'], kwargs['year']], fetch=True)[0]['total']
        return context


class AddTeachingHourView(OlympiadMixin, FormView):
    template_name = 'olympiad/add_teaching_hour.html'
    form_class = TeachingHourForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hours'] = run_query(
            "select st,en,day,en-st as time,(en-st)*hourly_wage as wage from teachinghour natural join course where cname=%s and fname=%s and year=%s",
            [self.kwargs['cname'], self.kwargs['fname'], self.kwargs['year']], fetch=True, raise_not_found=False)
        context['hourly_wage'] = \
        run_query("select hourly_wage from course where cname=%s and fname=%s and year=%s",
                  [self.kwargs['cname'], self.kwargs['fname'], self.kwargs['year']], fetch=True)[0]['hourly_wage']
        context['total_time'] = run_query(
            "select sum(en-st) as sum from teachinghour where cname=%s and fname=%s and year=%s",
            [self.kwargs['cname'], self.kwargs['fname'], self.kwargs['year']], fetch=True)[0]['sum']
        context['total_wage'] = run_query(
            "select sum((en-st)*hourly_wage) as total from course natural join teachinghour where cname=%s and fname=%s and year=%s",
            [self.kwargs['cname'], self.kwargs['fname'], self.kwargs['year']], fetch=True)[0]['total']
        return context

    def dispatch(self, request, *args, **kwargs):
        self.cname = kwargs['cname']
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('olympiad:course:add-teaching-hour', args=[self.fname, self.year,
                                                                  self.kwargs['cname']])

    def form_valid(self, form):
        data = form.cleaned_data
        run_query("insert into teachinghour(fname,year,cname,st,en,day) values(%s,%s,%s,%s,%s,%s)",
                  [self.fname, self.year, self.cname, data['st'], data['en'], data['day']])
        return super().form_valid(form)
