from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DeleteView

from .models import EmployeeDetails
from . import views
from django.shortcuts import render, get_object_or_404

import employe
from .models import *
from django.contrib.auth import login, logout, authenticate


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
        ec = request.POST['employeecode']
        department = request.POST['dept']
        contact = request.POST['contact']
        jdate = request.POST['jdate']

        employee.user.first_name = fn
        employee.user.last_name = ln
        employee.empcode = ec
        employee.dept = department
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
    if request.method == "POST":
        fn = request.POST['firstname']
        ln = request.POST['lastname']
        ec = request.POST['employeecode']
        em = request.POST['email']
        pw = request.POST['P']
        da = request.POST['jdate']

        try:
            user = User.objects.create_user(first_name=fn, last_name=ln, username=em, password=pw)
            EmployeeDetails.objects.create(user=user, empcode=ec)
            error = "no"
        except:
            error = "yes"
    return render(request, 'add_employee.html', locals())


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
