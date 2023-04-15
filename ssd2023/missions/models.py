from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

DEFAULT_NAME_LENGTH = 1024
DEFAULT_DESCRIPTION_LENGTH = 4096


class SecureCharField(models.CharField):
    """A wrapper for a CharField that encrypts the data before storing it in the database."""

    description = "A one-way encrypted secure character field. It cannot be decrypted, only verified"

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 104
        super().__init__(*args, **kwargs)

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value

        return "#########"

    def to_python(self, value):
        if value is None:
            return value

        return "#########"


class Division(models.Model):
    """A division of the organisation; contains one or more employees."""

    name = models.CharField(max_length=DEFAULT_NAME_LENGTH)

    def __str__(self):
        return self.name


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
    social_security_number = SecureCharField(blank=True, max_length=9)  # TODO: add fixed length
    security_clearance = models.IntegerField(choices=SecurityClearance.choices)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name


class Mission(models.Model):
    """A mission that the organisation is working on."""

    name = models.CharField(max_length=DEFAULT_NAME_LENGTH)
    description = models.CharField(blank=True, null=True, max_length=4096)
    division = models.ForeignKey(Division, null=True, on_delete=models.SET_NULL)
    supervisor = models.ForeignKey(Employee, on_delete=models.CASCADE)
    start_date = models.DateTimeField("Date of commencement", blank=True, null=True)
    end_date = models.DateTimeField("Date of completion", blank=True, null=True)
    security_clearance = models.IntegerField(choices=SecurityClearance.choices)

    def __str__(self):
        return self.name

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
        return self.mission.name + ": " + self.title


class Project(models.Model):
    """A project that the organisation is working on."""

    name = models.CharField(max_length=DEFAULT_NAME_LENGTH)
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE)
    manager = models.ForeignKey(Employee, null=True, on_delete=models.SET_NULL)
    location = models.CharField(max_length=100)
    start_date = models.DateTimeField("Date of commencement")
    end_date = models.DateTimeField("Date of completion")
    description = models.CharField(max_length=4096, blank=True, null=True)

    def __str__(self):
        return self.name

    def clean(self):
        if self.start_date and self.end_date:
            if self.end_date < self.start_date:
                raise ValidationError("End date-time must be later than start date-time.")
