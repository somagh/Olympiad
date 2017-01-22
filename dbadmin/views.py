from django.http import HttpResponse
from django.urls import reverse

from django.views.generic import FormView

from Olympiad.helpers import run_query
from dbadmin.forms import NewFeolForm, NewOlForm, RegisterForm, LoginForm , NewUniversityfieldForm


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
        print(self.request.session['user'])
        run_query(
            "insert into olympiad(fname, max_fail, year, m1_no, m2_no, manager) values(%s,%s,%s,%s,%s,%s)",
            [form.data['feol'], form.data['saghf'], form.data['yr'], form.data['t_m1'],
             form.data['t_m2'], form.data['manager']])
        return HttpResponse("المپیاد جدید با موفقیت اضافه شد")


class RegisterView(FormView):
    template_name = 'dbadmin/register.html'
    form_class = RegisterForm

    def get_success_url(self):
        return reverse('dbadmin:successful-signup')

    def form_valid(self, form):
        data = form.cleaned_data
        run_query('insert into human(national_code, name, password) values (%s, %s, %s)',
                  [data['national_code'], data['name'], data['password']])
        return super().form_valid(form)


class LoginView(FormView):
    template_name = 'dbadmin/login.html'
    form_class = LoginForm

    def get_success_url(self):
        return reverse('home')

    def form_valid(self, form):
        user = form.cleaned_data['user']
        self.request.session['user'] = user
        return super().form_valid(form)


class NewUniversityField(FormView):
    template_name = 'dbadmin/newUniversityfield.html'
    form_class = NewUniversityfieldForm

    def form_valid(self, form):
        run_query("insert into universityfield(id, gp_name, min_level, olympiad_capacity) values(%s,%s,%s,%s)",
                  [form.data['id'], form.data['group_name'],
                   form.data['min_level'], form.data['olympiad_capacity']])
        return HttpResponse("رشته دانشگاهی جدید با موفقیت اضافه شد")

