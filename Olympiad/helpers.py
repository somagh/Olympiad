from django.db import connection
from django.http.response import Http404
from django.urls import reverse


def run_query(query: object, params: object = None, fetch: object = False, raise_not_found: object = True) -> object:
    cursor = connection.cursor()
    cursor.execute(query, params)
    if fetch:
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()
        if raise_not_found and len(rows) == 0:
            raise Http404('صفحه مورد نظر یافت نشد')
        return [dict(zip(columns, row)) for row in rows]


class OlympiadMixin:
    def dispatch(self, request, *args, **kwargs):
        self.fname = kwargs['fname']
        self.year = kwargs['year']
        run_query('select fname from olympiad where fname=%s and year=%s and manager=%s',
                  [self.fname, self.year, request.session['user']['national_code']], fetch=True)
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('olympiad:home', args=[self.fname, self.year])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fname'] = self.fname
        context['year'] = self.year
        return context
