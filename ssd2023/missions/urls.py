from django.urls import path

from . import views

urlpatterns = [
    path("", views.index),
    path("login", views.login_endpoint),
    path("logout", views.logout_endpoint),
    path("mission/create", views.mission_create),
    path("mission/<int:mission_id>", views.mission_details),
    path("mission/<int:mission_id>/update", views.mission_update),
    path("mission/<int:mission_id>/delete", views.mission_delete),
    path("mission-report/generate/<int:mission_id>", views.mission_report_generate),
    path("mission-report/<int:mission_report_id>", views.mission_report_details),
]
