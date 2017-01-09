"""Olympiad URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from dbadmin.views import newFeol, NewOl, M1M2Date, AddProblemView, EditProblemView, \
    AddCourseView, EditCourseView, OlympiadView

problem_urlpatterns = [
    url(r'^$', AddProblemView.as_view(), name='add'),
    url(r'^(?P<pnum>\d+)/$', EditProblemView.as_view(), name='edit')
]

olympiad_urlpatterns = [
    url(r'^$', OlympiadView.as_view(), name='home'),
    url(r'^course/$', AddCourseView.as_view(), name='add-course'),
    url(r'^course/(?P<cname>\w+(-\w+)*)/$', EditCourseView.as_view(), name='edit-course'),
    url(r'^m1m2date/$', M1M2Date.as_view(), name='m1m2date'),
]

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^new-field/$',newFeol.as_view(), name='new-field'),
    url(r'^new-olympiad/$',NewOl.as_view(), name='new-olympiad'),
    url(r'^olympiad/(?P<fname>\w+(-\w+)*)/(?P<year>\d+)/', include(olympiad_urlpatterns, namespace='olympiad')),
    url(r'^problem/(?P<eid>\d+)/', include(problem_urlpatterns, namespace='problem')),
]
