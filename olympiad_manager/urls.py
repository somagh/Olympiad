from django.conf.urls import url, include

from olympiad_manager.views import ProblemListView, AddProblemView, EditProblemView, AddCourseView, \
    EditCourseView, OlympiadView, M1M2Date

problem_urlpatterns = [
    url(r'^$',ProblemListView.as_view(),name='list'),
    url(r'^add/$', AddProblemView.as_view(), name='add'),
    url(r'^(?P<pnum>\d+)/$', EditProblemView.as_view(), name='edit')
]

course_urlpatterns = [
    url(r'^add/$', AddCourseView.as_view(), name='add'),
    url(r'^(?P<cname>\w+(-\w+)*)/$', EditCourseView.as_view(), name='edit'),
]

olympiad_urlpatterns = [
    url(r'^$', OlympiadView.as_view(), name='home'),
    url(r'^course/', include(course_urlpatterns, namespace='course')),
    url(r'^m1m2date/$', M1M2Date.as_view(), name='m1m2date'),
    url(r'^problem/(?P<eid>\d+)/', include(problem_urlpatterns, namespace='problem')),
]
