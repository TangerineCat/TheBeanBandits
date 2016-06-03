from django.contrib import admin

# Register your models here.
from .models import Student, StudentHistory

admin.site.register(Student)
admin.site.register(StudentHistory)
