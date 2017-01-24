from django.conf.urls import url
from django.views.generic.base import TemplateView

from dbadmin.views import newFeol, NewOl, NewUniversityField, ScholarsList

urlpatterns = [
    url(r'^successful-signup/$', TemplateView.as_view(template_name='dbadmin/successful_signup.html')
        , name='successful-signup'),
    url(r'^new-field/$', newFeol.as_view(), name='new-field'),
    url(r'^new-olympiad/$', NewOl.as_view(), name='new-olympiad'),
    url(r'^scholars-list/$', ScholarsList.as_view(), name='scholars-list'),
    url(r'^new-universityfield/$', NewUniversityField.as_view(), name='new-university-field'),
]