# Generated by Django 5.1.3 on 2024-11-21 12:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Hall',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hall_name', models.CharField(max_length=50)),
                ('capacity', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Lecturer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('role', models.CharField(choices=[('Professor', 'Professor'), ('Senior Lecturer', 'Senior Lecturer'), ('Assistant Lecturer', 'Assistant Lecturer')], default='Assistant Lecturer', max_length=50)),
                ('weekly_limit', models.PositiveIntegerField(default=20)),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject_code', models.CharField(max_length=10, unique=True)),
                ('subject_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='SubjectLecturer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lecturer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='timetable.lecturer')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='timetable.subject')),
            ],
        ),
        migrations.CreateModel(
            name='TimetableEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.CharField(choices=[('1st Year', '1st Year'), ('2nd Year', '2nd Year'), ('3rd Year', '3rd Year'), ('4th Year', '4th Year')], max_length=10)),
                ('day', models.CharField(max_length=10)),
                ('time_slot', models.CharField(max_length=20)),
                ('hall', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='timetable.hall')),
                ('subject_lecturer', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='timetable.subjectlecturer')),
            ],
        ),
    ]
