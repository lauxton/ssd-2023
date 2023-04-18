"""Set admin privileges for admin page"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Division, Mission, MissionReport, Employee


admin.site.register(Division)
admin.site.register(Mission)
admin.site.register(MissionReport)


class EmployeeInline(admin.StackedInline):
    """Employee privileges"""
    model = Employee
    can_delete = False
    verbose_name_plural = 'employee'


class UserAdmin(BaseUserAdmin):
    """Admin privileges"""
    inlines = (EmployeeInline,)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
