from django.db import connection
from django.db.models import QuerySet
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.generic import FormView
from django.views.generic import TemplateView

from Olympiad.helpers import run_query
from dbadmin.forms import NewFeolForm, NewOlForm, M1M2DateForm


def test(request):
    cursor = connection.cursor()
    cursor.execute("select * from feol")
    columns = [col[0] for col in cursor.description]
    return HttpResponse([dict(zip(columns, row)) for row in cursor.fetchall()])


class newFeol(FormView):
    template_name = 'dbadmin/newFeol.html'
    form_class = NewFeolForm

    def form_valid(self, form):
        run_query("insert into feol(rname, t_t, t_n) values(%s,%s,%s)", [form.data['name'], form.data['t_t'],
                                                                         form.data['t_n']])
        groups = form.data['groups'].split('-')
        for group in groups:
            run_query("insert into olgp(rname, gpname) values(%s, %s)", [form.data['name'], group])
        return HttpResponse("رشته جدید با موفقیت اضافه شد")


class NewOl(FormView):
    form_class = NewOlForm
    template_name = 'dbadmin/newOl.html'

    def form_valid(self, form):
        run_query("insert into ol(rname, saghfeoftadan, yr, t_m1, t_m2) values(%s,%s,%s,%s,%s)",
                  [form.data['feol'], form.data['saghf'], form.data['yr'], form.data['t_m1'], form.data['t_m2']])
        return HttpResponse("المپیاد جدید با موفقیت اضافه شد")


class M1M2Date(FormView):
    template_name = 'dbadmin/m1m2date.html'
    form_class = M1M2DateForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['rname'] = self.request.GET.get('rname')
        kwargs['yr'] = self.request.GET.get('yr')
        return kwargs