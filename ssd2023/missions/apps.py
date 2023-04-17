"""Module for app configurations """
from django.apps import AppConfig


class MissionsConfig(AppConfig):
    """Configure the Missions App"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'missions'
