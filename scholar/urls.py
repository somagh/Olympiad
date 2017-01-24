from django.conf.urls import url

from scholar.views import RegisterOlympiad, RequestUniversityField

urlpatterns = [
    url(r'^register-olympiad/$', RegisterOlympiad.as_view(),name='register-olympiad'),
    url(r'^request-university-field/$', RequestUniversityField.as_view(), name='request-university-field'),
]