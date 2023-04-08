from django.db import models

DEFAULT_NAME_LENGTH = 1024
DEFAULT_DESCRIPTION_LENGTH = 4096

class SecureCharField(models.CharField):
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
    name = models.CharField(max_length=DEFAULT_NAME_LENGTH)

    def __str__(self):
         return self.name
    
class Employee(models.Model):
    firstName = models.CharField(max_length=256)
    lastName = models.CharField(max_length=256)
    division = models.ForeignKey(Division, on_delete=models.CASCADE)
    role = models.CharField(max_length=50, default="Unassigned")
    email = models.EmailField()
    _address = models.CharField(max_length=100)
    _phoneNumber = models.CharField(max_length=14)
    _socialSecurityNumber = SecureCharField()
    _securityClearance = models.SmallIntegerField()
    
    def __str__(self):
         return self.firstName + " " + self.lastName    

class Mission(models.Model):
    name = models.CharField(max_length=DEFAULT_NAME_LENGTH)
    division = models.ForeignKey(Division, on_delete=models.CASCADE)
    supervisor = models.ForeignKey(Employee, on_delete=models.CASCADE)
    startDate = models.DateTimeField("Date of commencement")
    endDate = models.DateTimeField("Date of completion")
    _description = models.CharField(max_length=4096)

    def __str__(self):
         return self.name        

class Report(models.Model):
    title = models.CharField(max_length=DEFAULT_NAME_LENGTH)
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE)
    assignedTo = models.ForeignKey(Employee, on_delete=models.CASCADE)
    publishDate = models.DateTimeField("Date published")
    _summary = models.CharField(max_length=DEFAULT_DESCRIPTION_LENGTH)

    def __str__(self):
         return self.mission.name + ": " + self.title

class Project(models.Model):
    name = models.CharField(max_length=DEFAULT_NAME_LENGTH)
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE)
    manager = models.ForeignKey(Employee, on_delete=models.CASCADE)
    location = models.CharField(max_length=100)
    startDate = models.DateTimeField("Date of commencement")
    endDate = models.DateTimeField("Date of completion")
    _description = models.CharField(max_length=4096)

    def __str__(self):
         return self.name


class Satellite(models.Model):
    name = models.CharField(max_length=DEFAULT_NAME_LENGTH)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    location = models.CharField(max_length=100)

    def __str__(self):
         return self.name
