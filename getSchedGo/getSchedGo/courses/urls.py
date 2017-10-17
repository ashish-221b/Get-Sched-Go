from django.conf.urls import url
from . import views
app_name = 'courses'
urlpatterns = [
    url(r"^$", views.CourseView, name="CourseView"),
    url(r"^some/(?P<pk1>\w+)/(?P<pk2>\w+)$", views.CourseView, name="some"),
    url(r"^list/$",views.Enrollmentview, name="Enrollmentview"),
    url(r"^(?P<pk>[0-9]+)/add/$",views.UserAdder, name="UserAdder"),
    url(r"^(?P<pk>[0-9]+)/remove/$",views.UserDropper, name="UserDropper"),
    # url(r"^(?P<pk>[0-9]+)/anyDay/$", views.TodayStats, name="AnyDayStatistics"),
    # url(r"^list/$", views.EventBeforeDate, name="EventBeforeDate"),
    # url(r"^donelist/$", views.CompletedList, name="CompletedList"),
    # url(r"^(?P<pk>[0-9]+)/comp/$", views.MarkItCompleted, name="MarkItCompleted"),
    url(r"^SelectCourse$", views.SelectCourse, name="SelectCourse"),
    url(r"^(?P<pk>[0-9]+)/ClaimCourse$", views.SelectCourse, name="ClaimCourse"),
    url(r"^(?P<pk>[0-9]+)/converttoevent$", views.AssignmentToEvent, name="AssignmentToEvent")
]
