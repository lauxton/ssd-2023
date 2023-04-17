"""Database and Class Models for the App"""
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django_cryptography.fields import encrypt

DEFAULT_NAME_LENGTH = 1024
DEFAULT_DESCRIPTION_LENGTH = 4096


class Division(models.Model):
    """A division of the organisation; contains one or more employees."""

    name = models.CharField(max_length=DEFAULT_NAME_LENGTH)

    def __str__(self):
        return str(self.name)


class SecurityClearance(models.IntegerChoices):
    """Possible security clearance for an employee or datum."""
    BASELINE = 1
    CONFIDENTIAL = 2
    SECRET = 3
    TOP_SECRET = 4


class Employee(models.Model):
    """
    A single employee record with a role and division.

    This is a 'Profile' model in Django that associates a User with additional information.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    division = models.ForeignKey(Division, null=True, on_delete=models.SET_NULL)
    address = models.CharField(blank=True, max_length=100)
    phone_number = models.CharField(blank=True, max_length=14)
    social_security_number = encrypt(models.CharField(blank=True, max_length=9))
    security_clearance = models.IntegerField(choices=SecurityClearance.choices)

    def __str__(self):
        if self.user.first_name and self.user.last_name:
            return self.user.first_name + " " + self.user.last_name

        return self.user.username


class Mission(models.Model):
    """A mission that the organisation is working on."""

    name = models.CharField(max_length=DEFAULT_NAME_LENGTH)
    description = models.CharField(blank=True, null=True, max_length=4096)
    division = models.ForeignKey(Division, null=True, on_delete=models.SET_NULL)
    supervisor = models.ForeignKey(Employee, on_delete=models.CASCADE, limit_choices_to={
                                   'user__groups__name': 'ISS_Admin_User'})
    start_date = models.DateTimeField("Date of commencement", blank=True, null=True)
    end_date = models.DateTimeField("Date of completion", blank=True, null=True)
    security_clearance = models.IntegerField(choices=SecurityClearance.choices)

    def __str__(self):
        return str(self.name)

    def clean(self):
        if self.start_date and self.end_date:
            if self.end_date < self.start_date:
                raise ValidationError("End date-time must be later than start date-time.")


class MissionReport(models.Model):
    """A report on a mission."""

    title = models.CharField(max_length=DEFAULT_NAME_LENGTH)
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(Employee, null=True, on_delete=models.SET_NULL)
    publish_date = models.DateTimeField("Date published")
    summary = models.CharField(max_length=DEFAULT_DESCRIPTION_LENGTH)

    def __str__(self):
        return str(self.title)
