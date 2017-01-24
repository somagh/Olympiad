from django.views.generic import FormView

from Olympiad.helpers import OlympiadMixin
from olympiad_manager.forms import LevelForm


class ManageLevelsView(OlympiadMixin,FormView):
    template_name = 'olympiad/levels.html'
    form_class = LevelForm
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['fname'] = self.fname
        kwargs['year'] = self.year
        return kwargs


