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

from dbadmin.views import test, newFeol, NewOl, M1M2Date, AddProblemView, EditProblemView

problem_urlpatterns = [
    url(r'^$', AddProblemView.as_view()),
    url(r'^(?P<pnum>\d+)/$', EditProblemView.as_view())
]

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^test/$',test),
    url(r'^new-field/$',newFeol.as_view()),
    url(r'^new-olympiad/$',NewOl.as_view()),
    url(r'^m1m2date/$', M1M2Date.as_view()),
    url(r'^problem/(?P<eid>\d+)/', include(problem_urlpatterns)),
]
