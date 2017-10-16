from django.conf.urls import include, url
from django.contrib import admin
from . import views
app_name = 'suggestion'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r"^(?P<pk>[0-9]+)/eventconversion$", views.ConvertToEvent, name="ConvertToEvent"),


]
# ^(?P<pk>[0-9]+)/edit$
   
