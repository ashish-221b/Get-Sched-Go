from django.conf.urls import url
from . import views
app_name = 'statistics'
urlpatterns = [
    url(r"^$", views.TodayStats, name="TodayStatistic"),
    url(r"^(?P<pk>[0-9]+)/anyDay/$", views.TodayStats, name="AnyDayStatistics"),
    url(r"^list/$", views.EventBeforeDate, name="EventBeforeDate"),
    url(r"^donelist/$", views.CompletedList, name="CompletedList"),
    url(r"^(?P<pk>[0-9]+)/comp/$", views.MarkItCompleted, name="MarkItCompleted"),
    # url(r"^create/$", views.CreateEvent, name="CreateEvent"),
    # url(r"^(?P<pk>[0-9]+)/edit$", views.CreateEvent, name="EditEvent"),
    # url(r"^(?P<pk>[0-9]+)/delete$", views.DeleteEvent, name="DeleteEvent"),
    # url(r"^(?P<pk>[0-9]+)/sort$", views.EventList, name="SortEvent"),
    # url(r'^today/$',views.Schedules, name = "Schedule"),
]
