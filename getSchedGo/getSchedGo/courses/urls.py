from django.conf.urls import url
from . import views
## name of app to call it's url without clash with other app's url. works as a namespaces
app_name = 'courses'
## list of all url's corresponding to type of get requests to access all the view 
urlpatterns = [
    url(r"^$", views.CourseView, name="CourseView"),
    url(r"^some/(?P<pk1>[a-zA-Z0-9_ ]+)/(?P<pk2>\w+)/$", views.CourseView, name="some"),
    url(r"^list/$",views.Enrollmentview, name="Enrollmentview"),
    url(r"^(?P<pk>[0-9]+)/add/$",views.UserAdder, name="UserAdder"),
    url(r"^(?P<pk>[0-9]+)/remove/$",views.UserDropper, name="UserDropper"),
    # url(r"^(?P<pk>[0-9]+)/anyDay/$", views.TodayStats, name="AnyDayStatistics"),
    # url(r"^list/$", views.EventBeforeDate, name="EventBeforeDate"),
    # url(r"^donelist/$", views.CompletedList, name="CompletedList"),
    # url(r"^(?P<pk>[0-9]+)/comp/$", views.MarkItCompleted, name="MarkItCompleted"),
    url(r"^EditCourse$", views.EditCourse, name="EditCourse"),
    url(r"^SelectCourse$", views.SelectCourse, name="SelectCourse"),
    url(r"^(?P<pk>[0-9]+)/ClaimCourse$", views.SelectCourse, name="ClaimCourse"),
    url(r"^(?P<pk>[0-9]+)/converttoevent$", views.AssignmentToEvent, name="AssignmentToEvent"),
    url(r"^(?P<pk>[0-9]+)/classtoevent$", views.ClassToEvent, name="ClassToEvent"),
    url(r"^(?P<pk>[0-9]+)/examtoevent$", views.ExamToEvent, name="ExamToEvent"),
    url(r"^(?P<pk>[0-9]+)/examppreptoevent$", views.ExamPrepToEvent, name="ExamPrepToEvent"),

]
