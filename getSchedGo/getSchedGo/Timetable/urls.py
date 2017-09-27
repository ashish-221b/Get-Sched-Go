from django.conf.urls import url
from . import views
app_name = 'Timetable'
urlpatterns = [
    url(r"^$", views.EventList, name="EventList"),
    url(r"^create/$", views.CreateEvent, name="CreateEvent"),
]
