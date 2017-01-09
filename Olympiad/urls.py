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

from dbadmin.views import newFeol, NewOl
from olympiad_manager.urls import olympiad_urlpatterns

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^new-field/$',newFeol.as_view(), name='new-field'),
    url(r'^new-olympiad/$',NewOl.as_view(), name='new-olympiad'),
    url(r'^olympiad/(?P<fname>\w+(-\w+)*)/(?P<year>\d+)/', include(olympiad_urlpatterns, namespace='olympiad')),
]

