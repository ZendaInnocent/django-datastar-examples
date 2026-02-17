from django.urls import path

from . import views

app_name = 'examples'

urlpatterns = [
    path('', views.index_view, name='index'),
]
