from django.urls import path

from . import views

urlpatterns = [
    path("", views.index),
    path("login", views.login),
    path("create-report", views.create_report),
    path("export-report/<int:report_id>", views.export_report),
]
