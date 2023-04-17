from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import *

admin.site.register(Division)
admin.site.register(Mission)
admin.site.register(MissionReport)


class EmployeeInline(admin.StackedInline):
    model = Employee
    can_delete = False
    verbose_name_plural = 'employee'


class UserAdmin(BaseUserAdmin):
    inlines = (EmployeeInline,)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
