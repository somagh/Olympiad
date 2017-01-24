from django.views.generic.base import TemplateView

from Olympiad.helpers import run_query, OlympiadMixin


class ResultsView(TemplateView):
    template_name = 'olympiad/results.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        m = self.request.GET.get('step')
        self.fname = kwargs['fname']
        self.year = kwargs['year']
        if m == '2':
            queryset = run_query('select scholar_id as id, name from m2_accepted join human on '
                                 'scholar_id=national_code where fname=%s and year=%s',
                                 [self.fname, self.year],
                                 fetch=True, raise_not_found=False)
            context['title'] = 'اسامی پذیرفته‌شدگان مرحله دوم المپیاد'
        elif m == '1':
            queryset = run_query('select scholar_id as id, name from m1_accepted join human on '
                                 'scholar_id=national_code where fname=%s and year=%s',
                                 [self.fname, self.year], fetch=True, raise_not_found=False)
            context['title'] = 'اسامی پذیرفته‌شدگان مرحله اول المپیاد'
        else:
            queryset = run_query('select national_code as id, name from participation natural join '
                                 'human where fname=%s and year=%s', [self.fname, self.year],
                                 fetch=True, raise_not_found=True)
            context['title'] = 'شرکنندگان المپیاد'
        context['queryset'] = queryset
        return context
