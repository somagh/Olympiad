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

from olympiad_manager.urls import olympiad_urlpatterns
from olympiad_manager.views.problem import GradeView
from scholar.views import RegisterOlympiad
from ysc.views import HomeView, LogoutView

urlpatterns = [
    url(r'^olympiad/(?P<fname>[^/]*)/(?P<year>\d+)/', include(olympiad_urlpatterns, namespace='olympiad')),
    url(r'^', include('dbadmin.urls', namespace='dbadmin')),
    url(r'^', include('scholar.urls', namespace='scholar')),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^grade/(?P<eid>\d+)/(?P<pnum>\d+)/$', GradeView.as_view(), name='grade'),
    url(r'^$', HomeView.as_view(), name='home'),
]

