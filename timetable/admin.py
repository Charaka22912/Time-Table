from django.contrib import admin
from .models import Subject, Lecturer, Hall, TimetableEntry, SubjectLecturer

# Register models to the admin site
admin.site.register(Subject)
admin.site.register(Lecturer)
admin.site.register(Hall)
admin.site.register(TimetableEntry)
admin.site.register(SubjectLecturer)

