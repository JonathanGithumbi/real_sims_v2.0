from django.contrib import admin

from student.models import AdmissionNumber, Student

admin.site.register(Student)
admin.site.register(AdmissionNumber)