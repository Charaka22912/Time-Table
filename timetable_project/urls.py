"""
URL configuration for timetable_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from timetable.views import login_view
from timetable.views import register_view,logout_view,timetable_view,save_timetable_entry,find_replacement_lecturer,clear_timetable_entry,workload_monitoring,leave_request

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", login_view, name='superuser_login'),
    path('register-superuser/', register_view, name='register_superuser'),
    path('timetable/', timetable_view, name="timetable"),
    path("logout/", logout_view, name="logout"),
    path("save_timetable_entry/", save_timetable_entry, name="save_timetable_entry"),
    path("find_replacement_lecturer/", find_replacement_lecturer, name="find_replacement_lecturer"),
    path("clear_timetable_entry/", clear_timetable_entry, name="clear_timetable_entry"),
    path("workload_monitoring/", workload_monitoring, name="workload_monitoring"),
    path("leave_request/", leave_request, name="leave_request"), # Ensure this import path is correct
]