from django.db import connection
from django.db.models import QuerySet
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.generic import FormView
from django.views.generic import TemplateView

from dbadmin.forms import NewFeolForm


def test(request):
    cursor=connection.cursor()
    cursor.execute("select * from emtehan")
    columns = [col[0] for col in cursor.description]
    return HttpResponse([dict(zip(columns,row)) for row in cursor.fetchall()])


class newFeol(FormView):
    template_name = 'dbadmin/newFeol.html'
    form_class = NewFeolForm

    def form_valid(self, form):
        cursor = connection.cursor()
        cursor.execute("insert into feol(rname, t_t, t_n) values(%s,%s,%s)", [form.data['name'], form.data['t_t'],
                                                                              form.data['t_n']])
        return HttpResponse("رشته جدید با موفقیت اضافه شد")