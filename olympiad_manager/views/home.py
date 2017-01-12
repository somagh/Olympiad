from django.views.generic import TemplateView

from Olympiad.helpers import OlympiadMixin


class OlympiadView(OlympiadMixin, TemplateView):
    template_name = 'olympiad/olympiad.html'
