from django.conf.urls import url
from . import views
app_name = 'courses'
urlpatterns = [
    url(r"^$", views.CourseView, name="CourseView"),
    url(r"^list/$",views.Enrollmentview, name="Enrollmentview"),
    # url(r"^(?P<pk>[0-9]+)/anyDay/$", views.TodayStats, name="AnyDayStatistics"),
    # url(r"^list/$", views.EventBeforeDate, name="EventBeforeDate"),
    # url(r"^donelist/$", views.CompletedList, name="CompletedList"),
    # url(r"^(?P<pk>[0-9]+)/comp/$", views.MarkItCompleted, name="MarkItCompleted"),
]
