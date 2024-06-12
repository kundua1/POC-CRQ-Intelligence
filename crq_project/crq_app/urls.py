from django.urls import path
from . import views
from django.conf import settings
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.index),
    path('home/', views.home),
    path('home/app-server-mapping/', views.app_server_mapping),
    path('home/project-manager/', views.project_manager_view)
]