from django.views.generic import FormView

from Olympiad.helpers import OlympiadMixin, run_query
from olympiad_manager.forms import LevelForm


class ManageLevelsView(OlympiadMixin,FormView):
    template_name = 'olympiad/levels.html'
    form_class = LevelForm
    def dispatch(self, request, *args, **kwargs):
        self.medalists = run_query("select scholar_id , name from summercamp_silver join human on scholar_id=national_code where year=%s and fname=%s", [kwargs['year'], kwargs['fname']],
                              fetch=True, raise_not_found=False) \
                    + run_query("select scholar_id , name from summercamp_bronze join human on scholar_id=national_code where year=%s and fname=%s", [kwargs['year'], kwargs['fname']],
                                fetch=True, raise_not_found=False)
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['fname'] = self.fname
        kwargs['year'] = self.year
        kwargs['medalists']=self.medalists
        return kwargs

    def form_valid(self, form):
        for medalist in self.medalists:
            id=medalist['scholar_id']
            level=form.cleaned_data[id]
            print(level)
            if(level==''):
                run_query("update scholar set level=null where id=%s",[id])
            else:
                run_query("update scholar set level=%s where id=%s", [level,id])
        return super().form_valid(form)
