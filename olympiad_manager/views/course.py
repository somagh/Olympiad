from django.urls import reverse
from django.views.generic import FormView, TemplateView

from Olympiad.helpers import OlympiadMixin, run_query
from olympiad_manager.forms import CourseForm


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
