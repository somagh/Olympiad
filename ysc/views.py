from django.http.response import HttpResponseRedirect
from django.urls import reverse
from django.views.generic.base import TemplateView, View


class HomeView(TemplateView):
    template_name = 'home.html'


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        del request.session['user']
        return HttpResponseRedirect(reverse('home'))