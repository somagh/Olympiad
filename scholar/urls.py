from django.conf.urls import url

from scholar.views import RegisterOlympiad, RequestUniversityField, RequestSilverUniversityField

urlpatterns = [
    url(r'^register-olympiad/$', RegisterOlympiad.as_view(),name='register-olympiad'),
    url(r'^request-university-field/$', RequestUniversityField.as_view(), name='request-university-field'),
    url(r'^request-university-field-silver/$', RequestSilverUniversityField.as_view(), name='request-university-field-silver'),
]