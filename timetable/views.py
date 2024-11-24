from django.http import JsonResponse
from django.shortcuts import render
from .models import TimetableEntry, Subject, Lecturer, Hall, SubjectLecturer
import json
import pprint
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import logout
# from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.utils.cache import add_never_cache_headers
from django.views.decorators.cache import cache_control


failed_attempts = {}

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
# @login_required

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check if the username exists
        user_exists = User.objects.filter(username=username).exists()
        if not user_exists:
            messages.error(request, 'Username does not exist.')
            return render(request, 'login.html')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Successful login
            login(request, user)
            failed_attempts.pop(username, None)  # Reset failed attempts for the user
            return redirect("timetable")  # Redirect to dashboard
        else:
            # Increment failed attempts
            if username in failed_attempts:
                failed_attempts[username] += 1
            else:
                failed_attempts[username] = 1

            # Check if the user has failed 3 times
            if failed_attempts[username] >= 3:
                # Delete the user
                user_to_delete = User.objects.filter(username=username).first()
                if user_to_delete:
                    user_to_delete.delete()
                failed_attempts.pop(username, None)  # Remove from tracking
                messages.error(request, 'Account deleted due to multiple failed login attempts.')
            else:
                messages.error(request, f'Incorrect password. {3 - failed_attempts[username]} attempts remaining.')

    return render(request, 'login.html')

def register_view(request):
       
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()  # Safely get username
        password = request.POST.get('password', '').strip()  # Safely get password
        email = request.POST.get('email', '').strip()        # Safely get email

        # Validate the input
        if not username:
            messages.error(request, 'Username is required.')
        elif not password:
            messages.error(request, 'Password is required.')
        elif not email:
            messages.error(request, 'Email is required.')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
        else:
            # Create superuser
            User.objects.create_superuser(username=username, email=email, password=password)
            messages.success(request, 'Superuser created successfully!')
            return redirect('/')  # Redirect to login page after successful registration

    return render(request, 'register.html')

def logout_view(request):
    logout(request)  # Logs out the user
    response = HttpResponseRedirect('/')  # Redirect to the root path
    add_never_cache_headers(response)  # Clear browser cache
    return response

def timetable_view(request):
    time_slots = ["8:00 - 10:00", "10:00 - 12:00", "1:00 - 3:00", "3:00 - 5:00"]
    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    years = ["1st Year", "2nd Year", "3rd Year", "4th Year"]

    # Initialize timetable data structure
    timetable_data = {
        day: {time_slot: {year: None for year in years} for time_slot in time_slots}
        for day in weekdays
    }

    # Populate timetable data with existing entries
    for entry in TimetableEntry.objects.select_related(
            'subject_lecturer', 'subject_lecturer__subject', 'subject_lecturer__lecturer', 'hall'):
        if entry.day in timetable_data and entry.time_slot in timetable_data[entry.day]:
            timetable_data[entry.day][entry.time_slot][entry.year] = entry

    # Get lecturers with workload monitoring
    lecturers = Lecturer.objects.all()
    for lecturer in lecturers:
        lecturer.allocated_hours = (
            TimetableEntry.objects.filter(subject_lecturer__lecturer=lecturer).count() * 2
        )  # Each slot = 2 hours

    context = {
        "time_slots": time_slots,
        "weekdays": weekdays,
        "years": years,
        "timetable_data": timetable_data,
        "subjects": Subject.objects.all(),
        "lecturers": lecturers,
        "halls": Hall.objects.all(),
    } 
    return render(request, "timetable.html", context)


def save_timetable_entry(request):
    if request.method == "POST":
        data = json.loads(request.body)

        day = data.get("date")
        time_slot = data.get("timeslot")
        year = data.get("year")
        subject_id = data.get("subject")
        lecturer_id = data.get("lecturer")
        hall_id = data.get("hall")
        timetable_entry_id = data.get("entryId")
        try:
            # Validate required fields
            if not all([day, time_slot, year, subject_id, lecturer_id, hall_id]):
                return JsonResponse({"status": "error", "message": "Missing required fields."})
            # Fetch related objects
            try:
                subject_lecturer = SubjectLecturer.objects.get(subject_id=subject_id, lecturer_id=lecturer_id)
            except SubjectLecturer.DoesNotExist:
                return JsonResponse({"status": "error", "message": "Invalid subject or lecturer combination."})
            try:
                hall = Hall.objects.get(id=hall_id)
            except Hall.DoesNotExist:
                return JsonResponse({"status": "error", "message": "Invalid hall ID."})
            # Check for duplication
            if TimetableEntry.objects.filter(day=day, time_slot=time_slot, year=year).exists():
                if TimetableEntry.objects.filter(day=day, time_slot=time_slot, subject_lecturer=subject_lecturer).exclude(id=timetable_entry_id).count() > 0:
                    return JsonResponse({"status": "error", "message": "Lecturer is already assigned in this time slot!"})
                
                if TimetableEntry.objects.filter(day=day, time_slot=time_slot, hall=hall).exclude(id=timetable_entry_id).count() > 0:
                    return JsonResponse({"status": "error", "message": "Hall is already booked for this time slot!"})
            else:
                if TimetableEntry.objects.filter(day=day, time_slot=time_slot, subject_lecturer=subject_lecturer).exists():
                    return JsonResponse({"status": "error", "message": "Lecturer is already assigned in this time slot!"})

                if TimetableEntry.objects.filter(day=day, time_slot=time_slot, hall=hall).exists():
                    return JsonResponse({"status": "error", "message": "Hall is already booked for this time slot!"})

            # Save or update the timetable entry
            timetable_entry, created = TimetableEntry.objects.update_or_create(
                day=day,
                time_slot=time_slot,
                year=year,
                defaults={
                    "subject_lecturer": subject_lecturer,
                    "hall": hall,
                },
            )
        except ValueError as error:
            return JsonResponse({"status": "error", "message": f"Invalid data: {error}"})
        except Exception as error:
            return JsonResponse({"status": "error", "message": "An error occurred while saving the timetable entry."})
        if created:
            return JsonResponse({"status": "success", "message": "Entry created successfully!"})
        else:
            return JsonResponse({"status": "success", "message": "Entry updated successfully!"})
    return JsonResponse({"status": "error", "message": "Invalid request."})



def find_replacement_lecturer(request):
    if request.method == "POST":
        data = json.loads(request.body)
        day = data.get("day")
        time_slot = data.get("time_slot")
        subject_id = data.get("subject")
        lecturer_id = data.get("lecturer")

        # Validate inputs
        if not all([day, time_slot, subject_id, lecturer_id]):
            return JsonResponse({"status": "error", "message": "Missing required fields."})
        
        try:
            subject_lecturer = SubjectLecturer.objects.get(subject_id=subject_id, lecturer_id=lecturer_id)
        except SubjectLecturer.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Invalid subject or lecturer combination."})

        # Get unavailable lecturers
        unavailable_lecturers = TimetableEntry.objects.filter(day=day, time_slot=time_slot).values_list('subject_lecturer__lecturer_id', flat=True)
        available_lecturers = Lecturer.objects.exclude(id__in=unavailable_lecturers)

        # Filter lecturers based on workload limits
        replacements = [
            {
                "id": lecturer.id,
                "name": lecturer.name,
                "allocated_hours": TimetableEntry.objects.filter(subject_lecturer__lecturer=lecturer).count() * 2,
                "weekly_limit": lecturer.weekly_limit,
            }
            for lecturer in available_lecturers
            if TimetableEntry.objects.filter(subject_lecturer__lecturer=lecturer).count() * 2 < lecturer.weekly_limit 
            and SubjectLecturer.objects.filter(lecturer=lecturer, subject_id=subject_id).exists()

        ]

        return JsonResponse({"status": "success", "replacements": replacements})

    return JsonResponse({"status": "error", "message": "Invalid request."})


def clear_timetable_entry(request):
    if request.method == "POST":
        day = request.POST.get("day")
        time_slot = request.POST.get("time_slot")
        year = request.POST.get("year")

        if not all([day, time_slot, year]):
            return JsonResponse({"status": "error", "message": "Missing required fields."})

        TimetableEntry.objects.filter(day=day, time_slot=time_slot, year=year).delete()
        return JsonResponse({"status": "success", "message": "Entry cleared successfully!"})

    return JsonResponse({"status": "error", "message": "Invalid request."})


def workload_monitoring(request):
    lecturers = Lecturer.objects.all()
    monitoring_data = [
        {
            "lecturer_name": lecturer.name,
            "role": lecturer.role,
            "allocated_hours": TimetableEntry.objects.filter(subject_lecturer__lecturer=lecturer).count() * 2,
            "weekly_limit": lecturer.weekly_limit,
        }
        for lecturer in lecturers
    ]
    return JsonResponse({"status": "success", "monitoring_data": monitoring_data})


def leave_request(request):
    if request.method == "POST":
        lecturer_id = request.POST.get("lecturer")
        day = request.POST.get("day")
        time_slot = request.POST.get("time_slot")

        # Validate required fields
        if not all([lecturer_id, day, time_slot]):
            return JsonResponse({"status": "error", "message": "Missing required fields."})

        # Find available replacements
        unavailable_lecturers = TimetableEntry.objects.filter(day=day, time_slot=time_slot).values_list('subject_lecturer__lecturer_id', flat=True)
        available_lecturers = Lecturer.objects.exclude(id__in=unavailable_lecturers)

        replacements = [
            {
                "id": lecturer.id,
                "name": lecturer.name,
                "role": lecturer.role,
                "allocated_hours": TimetableEntry.objects.filter(subject_lecturer__lecturer=lecturer).count() * 2,
                "weekly_limit": lecturer.weekly_limit,
            }
            for lecturer in available_lecturers
        ]

        return JsonResponse({"status": "success", "replacements": replacements})

    return JsonResponse({"status": "error", "message": "Invalid request."})