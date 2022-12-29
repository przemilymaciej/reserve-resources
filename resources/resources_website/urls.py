from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('requests', views.RequestView.as_view(), name='requests'),
    path('release_resources', views.release_resources, name='release_resources'),
    path('reserve_resources', views.reserve_resources, name='reserve_resources'),
]