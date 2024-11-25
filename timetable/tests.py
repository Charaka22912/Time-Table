from django.test import TestCase
from .models import Subject, Lecturer, Hall, TimetableEntry, SubjectLecturer
from django.urls import reverse

# Test class for Timetable-related functionality
class TimetableTests(TestCase):
    
    def setUp(self):
        # This function will set up data before each test
        self.subject = Subject.objects.create(subject_name="Math", subject_code="MTH101")
        self.lecturer = Lecturer.objects.create(name="Dr. John", role="Professor", weekly_limit=20)
        self.hall = Hall.objects.create(hall_name="Hall 1", capacity=50)
        self.subject_lecturer = SubjectLecturer.objects.create(subject=self.subject, lecturer=self.lecturer)

    def test_subject_creation(self):
        # This checks if the subject was created correctly
        self.assertEqual(self.subject.subject_name, "Math")
        self.assertEqual(self.subject.subject_code, "MTH101")

    def test_lecturer_creation(self):
        # This checks if the lecturer was created correctly
        self.assertEqual(self.lecturer.name, "Dr. John")
        self.assertEqual(self.lecturer.role, "Professor")

    def test_timetable_entry_creation(self):
        # This tests the creation of a timetable entry
        entry = TimetableEntry.objects.create(
            day="Monday",
            time_slot="8:00 - 10:00",
            year="1st Year",
            subject_lecturer=self.subject_lecturer,
            hall=self.hall
        )
        self.assertEqual(entry.day, "Monday")
        self.assertEqual(entry.time_slot, "8:00 - 10:00")
        self.assertEqual(entry.year, "1st Year")
        self.assertEqual(entry.subject_lecturer.subject.subject_name, "Math")
        self.assertEqual(entry.hall.hall_name, "Hall 1")

    def test_save_timetable_entry(self):
        # Simulate POST request to save timetable entry
        response = self.client.post(reverse('save_timetable_entry'), {
            'day': 'Monday',
            'time_slot': '8:00 - 10:00',
            'year': '1st Year',
            'subject_lecturer': self.subject_lecturer.id,
            'hall': self.hall.id,
        })

        # Check if the response is successful and entry is saved
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'success')
        self.assertEqual(response.json()['message'], 'Entry created successfully!')

    def test_workload_monitoring(self):
        # Create a timetable entry for the lecturer
        TimetableEntry.objects.create(
            day="Monday",
            time_slot="8:00 - 10:00",
            year="1st Year",
            subject_lecturer=self.subject_lecturer,
            hall=self.hall
        )

        # Check the lecturer’s workload
        lecturer = Lecturer.objects.get(id=self.lecturer.id)
        self.assertEqual(lecturer.allocated_hours, 2)  # 1 slot = 2 hours