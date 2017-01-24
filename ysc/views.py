from django.http.response import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import FormView
from django.views.generic.base import TemplateView, View

from Olympiad.helpers import run_query
from ysc.forms import RegisterForm, LoginForm


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        self.username = self.request.session.get('user', {}).get('national_code', '')
        context['olympiads'] = run_query('select fname, year, name from olympiad join human on '
                                         'manager=national_code', fetch=True, raise_not_found=False)
        context['my_olympiads'] = run_query('select fname, year from olympiad where '
                                            'manager=%s', [self.username], fetch=True,
                                            raise_not_found=False)
        context['isAdmin'] = self.username == "root"
        context['grader_problems'] = run_query('select eid, pnum, text from grading natural join '
                                               'problem where grader_id=%s', [self.username],
                                               fetch=True, raise_not_found=False)
        return context


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
        return reverse('ysc:home')

    def form_valid(self, form):
        user = form.cleaned_data['user']
        self.request.session['user'] = user
        return super().form_valid(form)


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        del request.session['user']
        return HttpResponseRedirect(reverse('ysc:home'))
