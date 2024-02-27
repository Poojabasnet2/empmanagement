import profile

from django.contrib import admin
from django.urls import path,include


from employe import views
from employe.views import *
app_name = 'employe'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',index,name='index'),

    # path('registration',registration,name='registration'),
    path('emp_login',emp_login,name='emp_login'),
    path('emp_home',emp_home,name='emp_home'),
    path('profile',profile,name='profile'),
    path('Logout',Logout,name='logout'),
    path('admin_login',admin_login,name='admin_login'),
    path('admin_home',admin_home,name='admin_home'),
    path('all_employee',all_employee,name='all_employee'),
    path('add_employee',add_employee,name='add_employee'),
    path('edit_employee/<int:pid>/', edit_employee, name='edit_employee'),
    path('delete/<int:pid>/', views.delete, name='delete'),

 ]
