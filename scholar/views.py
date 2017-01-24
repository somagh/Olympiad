from django.http import Http404
from django.urls import reverse
from django.views.generic import FormView

from Olympiad.helpers import run_query
from scholar.forms import RegisterOlympiadForm


class RegisterOlympiad(FormView):
    template_name='scholar/registed_olympiad.html'
    form_class = RegisterOlympiadForm
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['registered']=run_query("select fname,year from participation natural join olympiad where national_code=%s",[self.request.session['user']['national_code']],fetch=True,raise_not_found=False)
        context['not_registered']=run_query("select fname,year from olympiad where not exists(select * from participation where olympiad.fname=participation.fname and olympiad.year=participation.year and national_code=%s)",[self.request.session['user']['national_code']],fetch=True,raise_not_found=False)
        return context

    def get_success_url(self):
        return reverse('register-olympiad')

    def form_valid(self, form):
        data=form.cleaned_data
        run_query("insert into participation(national_code,fname,year) values(%s,%s,%s)",[self.request.session['user']['national_code'],data['fname'],data['year']])
        try:
            exist=run_query("select * from scholar where id=%s",[self.request.session['user']['national_code']],fetch=True)
        except Http404:
            run_query("insert into scholar(id) values (%s)",[self.request.session['user']['national_code']])
        return super().form_valid(form)