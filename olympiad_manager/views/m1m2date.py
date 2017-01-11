from django.urls import reverse
from django.urls import reverse
from django.views.generic import FormView

from Olympiad.helpers import run_query, OlympiadMixin
from olympiad_manager.forms import M1M2DateForm


class M1M2Date(OlympiadMixin, FormView):
    template_name = 'olympiad/m1m2date.html'
    form_class = M1M2DateForm

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['rname'] = self.fname
        kwargs['yr'] = self.year
        return kwargs

    def get_success_url(self):
        return reverse('olympiad:home', args=[self.fname, self.year])

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        kwargs['int_list'] = [i for i in range(
            run_query('select count(*) from examday where fname=%s and year=%s',
                      [self.fname, self.year], fetch=True, raise_not_found=False)[0]['count'])]
        kwargs['fname'] = self.fname
        kwargs['year'] = self.year
        return kwargs

    def get_success_url(self):
        return reverse('olympiad:home', args=[self.fname, self.year])

    def form_valid(self, form):
        print("salam")
        run_query(
            "update exam set edate=%s where eid=(select eid from m1 where fname=%s and year=%s)",
            [form.data['m1_date'], form.data['rname'], form.data['yr']])
        old_count = \
            run_query("select count(*) from examday natural join m2 where fname=%s and year=%s",
                      [form.data['rname'], form.data['yr']], fetch=True)[0]['count']
        counter = 0
        for i in range(int(form.data['m2_day_count'])):
            print(i)
            print(counter)
            if form.data['m2_' + str(i) + '_date'] == "":
                continue
            if counter < old_count:
                run_query(
                    "update examday set percentage=%s where fname=%s and year=%s and num=%s",
                    [form.data['m2_' + str(i) + '_darsad'], form.data['rname'], form.data['yr'],
                     counter])
            else:
                run_query(
                    "insert into examday(fname,year,num,percentage) values(%s,%s,%s,%s)",
                    [form.data['rname'], form.data['yr'], counter,
                     form.data['m2_' + str(i) + '_darsad']])
            run_query(
                "update exam set edate=%s where eid=(select eid from examday where fname=%s and year=%s and num=%s)",
                [form.data['m2_' + str(i) + '_date'], form.data['rname'], form.data['yr'], counter])
            counter += 1
        for i in range(counter, old_count):
            run_query(
                "delete from exam where eid=(select eid from examday where fname=%s and year=%s and num=%s)",
                [form.data['rname'], form.data['yr'], i])
        return super().form_valid(form)
