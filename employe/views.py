import datetime
from django.http import JsonResponse
from django.db.models import Sum
from django.db.models import Q
import random
from django.contrib import messages
from datetime import date



from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DeleteView

from .models import EmployeeDetails
from . import views
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User

import employe
from .models import *
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages

from .models import Employee_leave


def index(request):
    return render(request, 'index.html')


# def registration(request):
#     error = ""
#     if request.method == "POST":
#         fn = request.POST['firstname']
#         ln = request.POST['lastname']
#         ec = request.POST['employeecode']
#         em = request.POST['email']
#         pw = request.POST['P']
#         try:
#             user = User.objects.create_user(first_name=fn, last_name=ln, username=em, password=pw)
#             EmployeeDetails.objects.create(user = user, empcode=ec)
#             error = "no"
#         except:
#             error = "yes"
#     return render(request, 'registration.html',locals())

def emp_login(request):
    error = ""
    if request.method == 'POST':
        u = request.POST['email']
        v = request.POST['P']
        user = authenticate(username=u, password=v)
        if user:
            login(request, user)
            error = "no"
        else:
            error = "yes"

    return render(request, 'emp_login.html', locals())


def emp_home(request):
    if not request.user.is_authenticated:
        return redirect('emp_login')
    return render(request, 'emp_home.html')


def profile(request):
    if not request.user.is_authenticated:
        return redirect('emp_login')
    error = ""
    user = request.user
    employee = EmployeeDetails.objects.get(user=request.user)
    if request.method == "POST":
        fn = request.POST['firstname']
        ln = request.POST['lastname']
        ec = request.POST['empcode']
        department = request.POST['dept']
        contact = request.POST['contact']
        jdate = request.POST['jdate']

        employee.user.first_name = fn
        employee.user.last_name = ln
        employee.empcode = ec
        employee.empdept = department
        employee.contact = contact
        employee.joiningdate = jdate

        if jdate:
            employee.joiningdate = jdate

        try:
            employee.save()
            employee.user.save()

            error = "no"
        except:
            error = "yes"
    return render(request, 'profile.html', locals())


def Logout(request):
    logout(request)
    return redirect('index')


def admin_login(request):
    return render(request, 'admin_login.html')


def admin_login(request):
    error = ""
    if request.method == 'POST':
        u = request.POST['username']
        p = request.POST['Password']
        user = authenticate(username=u, password=p)
        if user:
            login(request, user)
            error = "no"
        else:
            error = "yes"
    return render(request, 'admin_login.html', locals())


def admin_home(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    return render(request, 'admin_home.html')


def all_employee(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    employee = EmployeeDetails.objects.all()
    return render(request, 'all_employee.html', locals())


# def add_employee(request):
#     if not request.user.is_authenticated:
#         return redirect('admin_login')
#     employee = EmployeeDetails.objects.all()
#     return render(request, 'add_employee.html',locals())



def add_employee(request):
    error = ""
    departments = Department.objects.all()  # Retrieve all departments
    if request.method == "POST":
        fn = request.POST.get('firstname')
        ln = request.POST.get('lastname')
        em = request.POST.get('email')
        pw = request.POST.get('P')
        da = request.POST.get('jdate')
        co = request.POST.get('contact')
        dept_id = request.POST.get('dept')

        try:
            #Generate empcode
            randomNumber = random.randint(1000, 9999)
            firstInitial = fn[0].upper()
            lastInitial = ln[0].upper()
            empcode = firstInitial + lastInitial + str(randomNumber)

            # Create the User instance
            user = User.objects.create_user(first_name=fn, last_name=ln, email=em, username=em, password=pw)
            # Get the Department instance
            department = Department.objects.get(id=dept_id)
            # Create the EmployeeDetails instance
            employee_details = EmployeeDetails.objects.create(user=user, empdept=department, joiningdate=da, empcode=empcode, contact=co)
            messages.success(request, 'Employee added successfully')

            error = "no"
        except Exception as e:
            error = str(e)

    # Check if the form was submitted successfully, if so, reset the error
    if error == "no":
        error = ""  # Reset error message after successful submission


    return render(request, 'add_employee.html', {'error': error, 'departments': departments})


def edit_employee(request, pid):
    error = ""
    employee = get_object_or_404(EmployeeDetails, id=pid)

    if request.method == "POST":
        fn = request.POST.get('firstname')
        ln = request.POST.get('lastname')
        ec = request.POST.get('employeecode')
        em = request.POST.get('email')
        pw = request.POST.get('P')
        da = request.POST.get('jdate')

        try:
            user = employee.user
            user.first_name = fn
            user.last_name = ln
            user.username = em
            user.set_password(pw)  # Use set_password to hash the password
            user.save()

            employee.empcode = ec
            employee.save()

            error = "no"
        except Exception as e:
            error = "yes"
            # Log the exception for debugging purposes
            print(e)

    return render(request, 'edit_employee.html', {'error': error, 'employee': employee})


def delete(request, pid):
    employee = get_object_or_404(EmployeeDetails, id=pid)

    if request.method == 'POST':
        employee.delete()
        return redirect('all_employee')

def leave(request):

    employee = get_object_or_404(EmployeeDetails, user=request.user)


    request_user = employee.user


    leave_history = Employee_leave.objects.filter(user=request_user)

    context = {
        'leave_history': leave_history
    }

    return render(request, 'leave.html', context)

def leave_request(request):
    if request.method == 'POST':
        start_date=request.POST.get('start')
        end_date=request.POST.get('end')
        Reason=request.POST.get('reason')

        current_user=request.user

        leave_request=Employee_leave.objects.create(

            user=current_user,
            start_date=start_date,
            End_date=end_date,
            message=Reason,
            status=0,
        )
        messages.success(request,'Request  sent successfully')

        return render(request,'leave.html')


def leave_view(request):
    employee_leave = Employee_leave.objects.all()

    for leave in employee_leave:
        leave.total_days = (leave.End_date - leave.start_date).days + 1

    context = {
        'employee_leave': employee_leave
    }

    return render(request, 'leave_view.html', context)


def approve_leave(request,id):
    leave=Employee_leave.objects.get(id=id)
    leave.status=1
    leave.save()
    return redirect(leave_view)

def Disapprove_leave(request,id):
    leave=Employee_leave.objects.get(id=id)
    leave.status=2
    leave.save()
    return redirect(leave_view)

def department(request):
    departments = Department.objects.all()

    if request.method == "POST":
        name = request.POST.get('dept')  # Assuming 'name' is the field name in your form

        # Create a new Department instance and save it
        new_department = Department(name=name)
        new_department.save()

        messages.success(request, 'Department successfully added')
        return redirect('department')  # Redirect to the same page after adding a department

    context = {
        'departments': departments,  # Pass the queryset to the template
    }
    return render(request, 'department.html', context)

def view_department(request):
    department=Department.objects.all()
    context={
        'department': department,
    }
    return render(request,'view_department.html',context)


def attendance(request):
    if request.method == "POST":
        employee_id = request.POST.get('emp')
        date = request.POST.get('date')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')

        if employee_id and date:
            try:
                employee = EmployeeDetails.objects.get(pk=employee_id)
                is_present = True if start_time and end_time else False
                attendance = Attendance(
                    user=employee.user,
                    date=date,
                    start_time=start_time,
                    end_time=end_time,
                    is_present=is_present
                )
                attendance.save()
                messages.success(request, 'Attendance successfully added')
            except EmployeeDetails.DoesNotExist:
                messages.error(request, 'Employee not found')
        else:
            messages.error(request, 'Incomplete data provided')

        return redirect('attendance')

    else:
        employees = EmployeeDetails.objects.all()
        return render(request, 'attendance.html', {'employees': employees})


def view_attendance(request):
    attendance = Attendance.objects.all()
    return render(request, 'view_attendance.html', {'attendance': attendance})

def skill(request):
    # skills = SkillSet.objects.all()  # Rename skill to skills for clarity

    if request.method == "POST":
        skill_name = request.POST.get('skill_name')
        proficiency_level = request.POST.get('proficiency_level')

        # Create a new SkillSet instance and save it
        new_skill = SkillSet(skill_name=skill_name, proficiency_level=proficiency_level)
        new_skill.save()

        messages.success(request, 'Skill successfully added')
        return redirect('skill_list')  # Redirect to the same page after adding a skill

    # context = {
    #     'skills': skills,  # Pass the queryset to the template
    # }
    return render(request,'skill.html')
def skill_list(request):
    skills = SkillSet.objects.all()
    return render(request, 'skill_list.html', {'skills': skills})

def edit_skill(request, pid):
    error = ""
    skill = get_object_or_404(SkillSet, id=pid)

    if request.method == "POST":
        Sn = request.POST.get('skill_name')
        Pn = request.POST.get('proficiency_level')

        try:
            skill.skill_name = Sn
            skill.proficiency_level = Pn
            skill.save()
            error = "no"
            # Redirect to the skill list page after successful update
            return redirect('skill_list')
        except Exception as e:
            error = "yes"
            # # Log the exception for debugging purposes
            # print(e)

    return render(request, 'edit_skill.html', {'error': error, 'skill': skill})


def calculate_salary(request):
    if request.method == "POST":
        employee_id = request.POST.get('employee_id')
        month = request.POST.get('month')
        year = request.POST.get('year')

        employee = get_object_or_404(EmployeeDetails, pk=employee_id)
        user = employee.user

        # Calculate total leave days in the selected month
        leave_days = \
        Employee_leave.objects.filter(user=user, status=1, start_date__year=year, start_date__month=month).aggregate(
            total_leave=Sum('total_days'))['total_leave'] or 0

        # Calculate total present days in the selected month
        present_days = Attendance.objects.filter(user=user, date__year=year, date__month=month, is_present=True).count()

        # Define salary parameters
        daily_rate = 1000  # Example daily rate
        paid_leave_days = 5  # Example paid leave days

        # Create or update the Salary record
        salary, created = Salary.objects.get_or_create(employee=employee, month=month, year=year)
        salary.present_days = present_days
        salary.leave_days = leave_days
        salary.calculate_salary(daily_rate, paid_leave_days)

        messages.success(request, f'Salary calculated successfully: {salary.amount}')

    employees = EmployeeDetails.objects.all()
    return render(request, 'calculate_salary.html', {'employees': employees})


def daily_attendance(request):
    if request.method == "POST":
        form = DailyAttendanceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Daily attendance successfully recorded')
            return redirect('daily_attendance')
    else:
        form = DailyAttendanceForm()
    return render(request, 'daily_attendance.html', {'form': form})


def calculate_monthly_summary():
    today = datetime.today()
    first_day_of_month = today.replace(day=1)
    last_day_of_last_month = first_day_of_month - timedelta(days=1)
    first_day_of_last_month = last_day_of_last_month.replace(day=1)

    employees = User.objects.all()
    for employee in employees:
        total_days = (last_day_of_last_month - first_day_of_last_month).days + 1
        attended_days = DailyAttendance.objects.filter(
            employee=employee,
            date__range=(first_day_of_last_month, last_day_of_last_month),
            is_present=True
        ).count()

        summary, created = MonthlySummary.objects.get_or_create(
            employee=employee,
            month=first_day_of_last_month,
            defaults={'total_days': total_days, 'attended_days': attended_days}
        )
        if not created:
            summary.total_days = total_days
            summary.attended_days = attended_days
            summary.save()


def monthly_summary(request):
    today = datetime.today()
    first_day_of_month = today.replace(day=1)
    last_day_of_last_month = first_day_of_month - timedelta(days=1)
    first_day_of_last_month = last_day_of_last_month.replace(day=1)

    summaries = MonthlySummary.objects.filter(month=first_day_of_last_month)
    return render(request, 'monthly_summary.html', {'summaries': summaries})
