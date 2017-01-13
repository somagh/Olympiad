from django.conf.urls import url
from django.views.generic.base import TemplateView

from dbadmin.views import newFeol, NewOl, RegisterView, LoginView , newUniversityfield

urlpatterns = [
    url(r'^signup/$', RegisterView.as_view(), name='register'),
    url(r'^successful-signup/$', TemplateView.as_view(template_name='dbadmin/successful_signup.html')
        , name='successful-signup'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^new-field/$', newFeol.as_view(), name='new-field'),
    url(r'^new-olympiad/$', NewOl.as_view(), name='new-olympiad'),
    url(r'^new-universityfield/$', newUniversityfield.as_view(), name='new-university-field'),
]