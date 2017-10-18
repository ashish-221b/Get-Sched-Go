from django.conf.urls import url
from . import views
app_name = 'statistics'
urlpatterns = [
    url(r"^$", views.TodayStats, name="TodayStatistic"),
    url(r"^(?P<pk>[0-9]+)/anyDay/$", views.TodayStats, name="AnyDayStatistics"),
    url(r"^list/$", views.EventBeforeDate, name="EventBeforeDate"),
    url(r"^donelist/$", views.CompletedList, name="CompletedList"),
    url(r"^(?P<pk>[0-9]+)/comp/$", views.MarkItCompleted, name="MarkItCompleted"),
    url(r"^csvlist/$", views.AheadOfTime, name="AheadOfTime"),
    url(r"^google/$",views.googleConnector, name="googleConnector")
    
]
