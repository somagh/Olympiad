from django.conf.urls import url, include

from olympiad_manager.views.levels import ManageLevelsView
from olympiad_manager.views.course import AddCourseView, EditCourseView, AddTeachingHourView, \
    TeachingHourListView
from olympiad_manager.views.course import CourseListView
from olympiad_manager.views.home import OlympiadView
from olympiad_manager.views.m1m2date import M1M2Date
from olympiad_manager.views.problem import ProblemListView, AddProblemView, EditProblemView, \
    ManageGraderView, \
    DeleteGraderView, GradeView, ExamResultsView
from olympiad_manager.views.results import ResultsView, Medalsview
from olympiad_manager.views.summer_exam import SummerExamListView, AddSummerExamView, \
    EditSummerExamView

problem_urlpatterns = [
    url(r'^$', ProblemListView.as_view(), name='list'),
    url(r'^results/$', ExamResultsView.as_view(), name='results'),
    url(r'^add/$', AddProblemView.as_view(), name='add'),
    url(r'^(?P<pnum>\d+)/graders/$', ManageGraderView.as_view(), name='graders'),
    url(r'^(?P<pnum>\d+)/graders/delete/$', DeleteGraderView.as_view()),
    url(r'^(?P<pnum>\d+)/$', EditProblemView.as_view(), name='edit'),
]

course_urlpatterns = [
    url(r'^$', CourseListView.as_view(), name='list'),
    url(r'^add/$', AddCourseView.as_view(), name='add'),
    url(r'^(?P<cname>[^/]*)/$', EditCourseView.as_view(), name='edit'),
    url(r'^(?P<cname>[^/]*)/add-teaching-hour/$', AddTeachingHourView.as_view(),
        name='add-teaching-hour'),
    url(r'^(?P<cname>[^/]*)/teaching-hours/$', TeachingHourListView.as_view(),
        name='teaching-hours')
]

summer_exam_urlpatterns = [
    url(r'^$', SummerExamListView.as_view(), name='list'),
    url(r'^add/$', AddSummerExamView.as_view(), name='add'),
    url(r'^(?P<eid>\d+)/$', EditSummerExamView.as_view(), name='edit'),
]

olympiad_urlpatterns = [
    url(r'^$', OlympiadView.as_view(), name='home'),
    url(r'^course/', include(course_urlpatterns, namespace='course')),
    url(r'^summer-exam/', include(summer_exam_urlpatterns, namespace='summer-camp-exam')),
    url(r'^m1m2date/$', M1M2Date.as_view(), name='m1m2date'),
    url(r'^results/$', ResultsView.as_view(), name='results'),
    url(r'^medals/$', Medalsview.as_view(), name='medals'),
    url(r'^problem/(?P<eid>\d+)/', include(problem_urlpatterns, namespace='problem')),
    url(r'^levels/$', ManageLevelsView.as_view(), name="levels"),
]
