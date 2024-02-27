from django.db import models

from django.contrib.auth.models import  User

class EmployeeDetails(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    empcode = models.IntegerField(null=True)
    empdept = models.CharField(max_length=50,null=True)

    contact = models.CharField(max_length=50,null=True)

    joiningdate = models.DateField(null=True)

    def __str__(self):
        return self.user.username

