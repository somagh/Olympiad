from django.conf.urls import url

from ysc.views import LogoutView, HomeView
from ysc.views import RegisterView, LoginView

urlpatterns =[
    url(r'^signup/$', RegisterView.as_view(), name='register'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^$', HomeView.as_view(), name='home'),
]