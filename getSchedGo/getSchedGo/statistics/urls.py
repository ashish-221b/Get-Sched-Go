from django.conf.urls import url
from . import views
## app_name helps django index urls mentioned below and for calling
# these urls is app_name:urlName. this helps developers forget the name they might have given
# to an app in different app 
app_name = 'statistics'
## These are list urlPatterns for this app. Ones containing 
# pk are the ones carrying parameters to corresponding view to do something specific
# for different call of same view with different parameters
urlpatterns = [
    url(r"^$", views.TodayStats, name="TodayStatistic"),
    url(r"^(?P<pk>[0-9]+)/anyDay/$", views.TodayStats, name="AnyDayStatistics"),
    url(r"^list/$", views.EventBeforeDate, name="EventBeforeDate"),
    url(r"^donelist/$", views.CompletedList, name="CompletedList"),
    url(r"^(?P<pk>[0-9]+)/comp/$", views.MarkItCompleted, name="MarkItCompleted"),
    url(r"^csvlist/$", views.AheadOfTime, name="AheadOfTime"),
    url(r"^google/$",views.googleConnector, name="googleConnector")
    
]
