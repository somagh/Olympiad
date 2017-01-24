from django.contrib.messages.views import SuccessMessageMixin
from django.forms import Form
from django.http.response import Http404
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

from Olympiad.helpers import OlympiadMixin, run_query


class OlympiadView(SuccessMessageMixin, OlympiadMixin, FormView):
    template_name = 'olympiad/olympiad.html'
    success_message = 'دانش‌پژوهان با موفقیت در بنیاد ملی نخبگان ثبت‌نام شدند'
    form_class = Form

    def get_success_url(self):
        return reverse('olympiad:home', args=[self.fname, self.year])

    def form_valid(self, form):
        scholars = run_query('select scholar_id from m2_accepted where fname=%s and year=%s',
                  [self.fname, self.year], fetch=True, raise_not_found=False)
        for scholar in scholars:
            try:
                run_query('select national_code from bmn where national_code=%s', [scholar['scholar_id']],
                          fetch=True)
            except Http404:
                run_query('insert into bmn(national_code) values(%s)', [scholar['scholar_id']])
        return super().form_valid(form)
