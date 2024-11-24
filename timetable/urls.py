from django.urls import path
from . import views

urlpatterns = [
    path("", views.timetable_view, name="timetable"),
    path("save_timetable_entry/", views.save_timetable_entry, name="save_timetable_entry"),
    path("find_replacement_lecturer/", views.find_replacement_lecturer, name="find_replacement_lecturer"),
    path("clear_timetable_entry/", views.clear_timetable_entry, name="clear_timetable_entry"),
    path("workload_monitoring/", views.workload_monitoring, name="workload_monitoring"),
    path("leave_request/", views.leave_request, name="leave_request"),
]