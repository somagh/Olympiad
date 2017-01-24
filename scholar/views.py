from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.views.generic import FormView

from Olympiad.helpers import run_query
from scholar.forms import RegisterOlympiadForm, RequestUniversityFieldForm


class RegisterOlympiad(FormView):
    template_name = 'scholar/registed_olympiad.html'
    form_class = RegisterOlympiadForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['registered'] = run_query(
            "select fname,year from participation natural join olympiad where national_code=%s",
            [self.request.session['user']['national_code']], fetch=True, raise_not_found=False)
        context['not_registered'] = run_query(
            "select fname,year from olympiad where not exists(select * from participation where olympiad.fname=participation.fname and olympiad.year=participation.year and national_code=%s)",
            [self.request.session['user']['national_code']], fetch=True, raise_not_found=False)
        return context

    def get_success_url(self):
        return reverse('register-olympiad')

    def form_valid(self, form):
        data = form.cleaned_data
        run_query("insert into participation(national_code,fname,year) values(%s,%s,%s)",
                  [self.request.session['user']['national_code'], data['fname'], data['year']])
        return super().form_valid(form)


class RequestUniversityField(SuccessMessageMixin, FormView):
    template_name = 'scholar/request_university_field.html'
    form_class = RequestUniversityFieldForm
    success_message = 'شما با موفقیت در رشته مدنظر ثبت نام شدید'

    def get_success_url(self):
        return reverse('home')

    def dispatch(self, request, *args, **kwargs):
        self.groups = run_query('select gp_name from groups where fname in (select fname from '
                                'summercamp_gold where scholar_id=%s)',
                                [request.session['user']['national_code']], fetch=True,
                                raise_not_found=False)
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['groups'] = self.groups
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_gold'] = self.groups != []
        return context

    def form_valid(self, form):
        run_query('update scholar set university_field_id=%s where id=%s',
                  [form.cleaned_data['field'], self.request.session['user']['national_code']])
        return super().form_valid(form)
