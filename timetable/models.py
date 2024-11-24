from django.db import models

# Subject Table
class Subject(models.Model):
    subject_code = models.CharField(max_length=10, unique=True)  # Unique subject code
    subject_name = models.CharField(max_length=100)  # Name of the Subject

    def __str__(self):
        return self.subject_name


# Lecturer Table# Lecturer Table
class Lecturer(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(
        max_length=50,
        choices=[
            ('Professor', 'Professor'),
            ('Senior Lecturer', 'Senior Lecturer'),
            ('Assistant Lecturer', 'Assistant Lecturer')
        ],
        default='Assistant Lecturer'  # Set default value here
    )
    weekly_limit = models.PositiveIntegerField(default=20)  # Default value for weekly limit

    def __str__(self):
        return self.name


# Subject_Lecturer Table (Mapping Table)
class SubjectLecturer(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)  # ForeignKey to Subject
    lecturer = models.ForeignKey(Lecturer, on_delete=models.CASCADE)  # ForeignKey to Lecturer

    def __str__(self):
        return f"{self.lecturer} - {self.subject}"


# Hall Table
class Hall(models.Model):
    hall_name = models.CharField(max_length=50)  # Name or Number of the Hall
    capacity = models.PositiveIntegerField()  # Capacity of the Hall

    def __str__(self):
        return self.hall_name


# TimetableEntry Table
class TimetableEntry(models.Model):
    year_choices = [
        ("1st Year", "1st Year"),
        ("2nd Year", "2nd Year"),
        ("3rd Year", "3rd Year"),
        ("4th Year", "4th Year"),
    ]
    year = models.CharField(max_length=10, choices=year_choices)  # Year
    day = models.CharField(max_length=10)  # Day of the Week
    time_slot = models.CharField(max_length=20)  # Time Slot
    subject_lecturer = models.ForeignKey(SubjectLecturer, on_delete=models.CASCADE,  null=True, blank=True, default=None )  # Map Subject-Lecturer
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE)  # Map Hall

    def __str__(self):
        return f"{self.year} - {self.day} - {self.time_slot}"