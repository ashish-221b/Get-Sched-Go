from django.conf.urls import url
from . import views
app_name = 'Timetable'
urlpatterns = [
    url(r"^$", views.EventList, name="EventList"),
    url(r"^create/$", views.CreateEvent, name="CreateEvent"),
    url(r"^(?P<pk>[0-9]+)/edit$", views.CreateEvent, name="EditEvent"),
    url(r"^(?P<pk>[0-9]+)/delete$", views.DeleteEvent, name="DeleteEvent"),
    url(r"^(?P<pk>[0-9]+)/desched$", views.DescheduleEvent, name="DescheduleEvent"),
    url(r"^(?P<pk>[0-9]+)/sort$", views.EventList, name="SortEvent"),
    url(r"^CreateAssignment$", views.CreateAssignment, name="CreateAssignment"),
    url(r"^Assignments$", views.Assignments, name="AssignmentList"),
    url(r"^(?P<pk>[0-9]+)/SortAssignment$", views.Assignments, name="SortAssignment"),
    url(r"^CreateClass$", views.CreateClass, name="CreateClass"),
    url(r"^Classes$", views.Classes, name="ClassList"),
    url(r"^(?P<pk>[0-9]+)/SortClass$", views.Classes, name="SortClass"),
    url(r"^CreateExam$", views.CreateExam, name="CreateExam"),
    url(r"^Exams$", views.Exams, name="ExamList"),
    url(r"^(?P<pk>[0-9]+)/SortExam$", views.Exams, name="SortExam"),
    url(r'^today/$',views.Schedules, name = "Schedule"),
   
]
