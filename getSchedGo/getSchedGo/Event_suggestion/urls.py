from django.conf.urls import include, url
from django.contrib import admin
from . import views
app_name = 'Suggstions'
urlpatterns = [
    url(r'^$', views.index, name='index'),
]
