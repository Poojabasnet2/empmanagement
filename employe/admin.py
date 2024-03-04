from django.contrib import admin
from .models import EmployeeDetails, Employee_leave,Department
# Register your models here.
admin.site.register(EmployeeDetails)
admin.site.register(Employee_leave)
admin.site.register(Department)
# admin.site.register(Leave)
# admin.site.register(Experience)
