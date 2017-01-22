from django.http.response import HttpResponseRedirect
from django.urls import reverse
from django.views.generic.base import TemplateView, View

from Olympiad.helpers import run_query


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['olympiads'] = run_query('select fname, year, name from olympiad join human on '
                                         'manager=national_code', fetch=True)
        return context

class LogoutView(View):
    def get(self, request, *args, **kwargs):
        del request.session['user']
        return HttpResponseRedirect(reverse('home'))