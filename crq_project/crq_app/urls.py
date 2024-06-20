from django.urls import path
from . import views
from django.conf import settings
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.index),
    path('login', views.handleLogin, name="handleLogin"),
    path('home/', views.home),
    path('home/logout/', LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL}, name='handleLogout'),
    path('home/app-server-mapping/', views.app_server_mapping),
    path('home/project-team/', views.project_team_view),
    path('home/app-owner/', views.app_owner_view)
]