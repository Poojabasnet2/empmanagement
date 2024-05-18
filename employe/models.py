

from django.db import models
from datetime import datetime



from django.contrib.auth.models import User


class EmployeeDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    empcode = models.CharField(max_length=20, null=True)
    empdept = models.CharField(max_length=50, null=True)

    contact = models.IntegerField(max_length=50, null=True)

    joiningdate = models.DateField(null=True)

    def __str__(self):
        return self.user.username


class Employee_leave(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    data = models.CharField(max_length=50)
    message = models.TextField()
    status = models.IntegerField(default=0)
    start_date = models.DateField(null=True)
    End_date = models.DateField(null=True)
    total_days = models.IntegerField(null=True)

    # def save(self, *args, **kwargs):
    #     if self.start_date and self.End_date:
    #         self.total_days = (self.End_date - self.start_date).days + 1
    #     super().save(*args, **kwargs)

    # def save(self, *args, **kwargs):
    #     if self.start_date and self.End_date:
    #
    #         # Calculate total days
    #         total_days = (self.End_date - self.start_date).days + 1
    #         self.total_days = total_days
    #     super().save(*args, **kwargs)
    #     return self

    def __str__(self):
        return str(self.user)


class Department(models.Model):
    name=models.CharField(max_length=100)

    def __str__(self):
        return self.name



class Attendance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField(null=True)  # No default value provided
    start_time = models.TimeField(null=True)  # No default value provided
    end_time = models.TimeField(null=True)
    is_present = models.BooleanField(default=False)  # Add this field


    def __str__(self):
        return f"{self.user.username} - {self.date}"

    class MonthlySummary(models.Model):
        employee = models.ForeignKey(User, on_delete=models.CASCADE)
        month = models.DateField()  # Use the first day of the month
        total_days = models.PositiveIntegerField()
        attended_days = models.PositiveIntegerField()

        @property
        def attendance_percentage(self):
            return (self.attended_days / self.total_days) * 100 if self.total_days else 0

    # def __str__(self):
    #     return str(self.user)



class SkillSet(models.Model):
    # user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    id = models.AutoField(primary_key=True,null=False)
    skill_name = models.CharField(max_length=100,null=False)
    proficiency_level = models.CharField(max_length=50,null=False)  # You can change this to whatever type you prefer

    def __str__(self):
        return f"{self.skill_name} - {self.proficiency_level}"


class Salary(models.Model):
    MONTH_CHOICES = [
        ('01', 'January'),
        ('02', 'February'),
        ('03', 'March'),
        ('04', 'April'),
        ('05', 'May'),
        ('06', 'June'),
        ('07', 'July'),
        ('08', 'August'),
        ('09', 'September'),
        ('10', 'October'),
        ('11', 'November'),
        ('12', 'December'),
    ]

    employee = models.ForeignKey(EmployeeDetails, on_delete=models.CASCADE)
    date = models.DateField(null=True)
    month = models.CharField(max_length=2, choices=MONTH_CHOICES, default='01')  # Default value set to '01' (January)
    salary = models.IntegerField(default=0)
    present_day = models.IntegerField(default=0)
    leave = models.IntegerField(default=0)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    PAID_LEAVE_DAYS = 5  # Define the number of paid leave days

    def save(self, *args, **kwargs):
        total_days_in_month = 30  # Assuming 30 days in a month
        daily_salary_rate = 1000  # Example daily salary rate
        leave_penalty = 1000  # Penalty for each unpaid leave day

        # Calculate the number of unpaid leave days
        unpaid_leave_days = max(self.leave - self.PAID_LEAVE_DAYS, 0)

        # Calculate the amount based on present days and unpaid leave days
        self.amount = (self.present_day * daily_salary_rate) - (unpaid_leave_days * leave_penalty)

        super().save(*args, **kwargs)

    # def save(self, *args, **kwargs):
    #     # Automatically calculate amount based on present_day and a fixed total days in a month
    #     total_days_in_month = 30  # Assuming there are always 30 days in a month
    #     daily_salary_rate = 1000  # Salary rate per day
    #     leave_penalty = 500  # Deduction for each leave day
    #
    #     # Calculate the number of working days
    #     working_days = total_days_in_month - self.leave
    #
    #     # Calculate the amount based on the number of present days
    #     self.amount = working_days * daily_salary_ratec
    #
    #     # Call the superclass's save method to save the Salary object
    #     super().save(*args, **kwargs)
