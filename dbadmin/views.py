from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, HttpResponseForbidden
from django.urls import reverse

from django.views.generic import FormView
from django.views.generic.base import TemplateView

from Olympiad.helpers import run_query
from dbadmin.forms import NewFeolForm, NewOlForm, NewUniversityfieldForm


class AdminPermission:
    def dispatch(self, request, *args, **kwargs):
        if self.request.session['user']['national_code'] != 'root':
            return HttpResponseForbidden('دسترسی به این صفحه ممنوع است')
        return super().dispatch(request, *args, **kwargs)


class newFeol(AdminPermission, FormView):
    template_name = 'dbadmin/newFeol.html'
    form_class = NewFeolForm

    def get_success_url(self):
        return reverse('ysc:home')

    def form_valid(self, form):
        run_query("insert into field(fname, gold_no, silver_no) values(%s,%s,%s)",
                  [form.data['name'], form.data['t_t'],
                   form.data['t_n']])
        groups = form.data['groups'].split('-')
        for group in groups:
            run_query("insert into groups(fname, gp_name) values(%s, %s)",
                      [form.data['name'], group])
        return super().form_valid(form)


class NewOl(AdminPermission, FormView):
    form_class = NewOlForm
    template_name = 'dbadmin/newOl.html'

    def get_success_url(self):
        return reverse('ysc:home')

    def form_valid(self, form):
        print(self.request.session['user'])
        run_query(
            "insert into olympiad(fname, max_fail, year, m1_no, m2_no, manager) values(%s,%s,%s,%s,%s,%s)",
            [form.data['feol'], form.data['saghf'], form.data['yr'], form.data['t_m1'],
             form.data['t_m2'], form.data['manager']])
        return super().form_valid(form)


class ScholarsList(AdminPermission, TemplateView):
    template_name = 'dbadmin/scholars.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['scholars'] = run_query(
            'select national_code as id, Human.name, UniversityField.name '
            'as uname from bmn '
            'natural join Human join scholar on '
            'national_code=scholar.id left join '
            'UniversityField on '
            'university_field_id=UniversityField.id', fetch=True,
            raise_not_found=False)
        return context


class NewUniversityField(SuccessMessageMixin, AdminPermission, FormView):
    template_name = 'dbadmin/newUniversityfield.html'
    form_class = NewUniversityfieldForm
    success_message = 'رشته دانشگاهی جدید با موفقیت اضافه شد'

    def get_success_url(self):
        return reverse('ysc:home')

    def form_valid(self, form):
        run_query(
            "insert into universityfield(id, gp_name, min_level, olympiad_capacity, name) values(%s,%s,%s,%s, %s)",
            [form.data['id'], form.data['group_name'],
             form.data['min_level'], form.data['olympiad_capacity'], form.data['name']])
        return super().form_valid(form)


class FieldRequests(AdminPermission, FormView):
    template_name = 'dbadmin/field-requests.html'
    form_class = NewUniversityfieldForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        q = run_query(
            'select national_code, human.name, field_id, level, min_level, olympiad_capacity, '
            'universityfield.name as uname from human join scholar on national_code=scholar.id '
            'natural join '
            'universityfieldpriority join universityfield on field_id=universityfield.id '
            'order by level desc', fetch=True,
            raise_not_found=False)
        count = {}
        out = []
        for h in q:
            current = count.get(h['field_id'], 0)
            if h['olympiad_capacity'] - current >= 0:
                if h['level'] and int(h['level']) * 1.25 >= h['min_level']:
                    run_query('update scholar set university_field_id=%s where id=%s',
                              [h['field_id'], h['national_code']])
                    count[h['field_id']] = current + 1
                    out.append({'name': h['name'], 'uname': h['uname']})
        context['scholars'] = out
        return context