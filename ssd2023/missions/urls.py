from django.urls import path

from . import views

urlpatterns = [
    path("", views.index),
    path("login", views.login_endpoint),
    path("logout", views.logout_endpoint),
    path("mission/<int:mission_id>", views.mission_details),
]
