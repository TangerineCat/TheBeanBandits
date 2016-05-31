from __future__ import unicode_literals

# Models the Student

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# Proficiency
NONE = 0
SOME = 1
FEW_YEARS = 2
SPEAK = 3
FLUENT = 4
READANDWRITE = 5
PROFICIENCY_CHOICES = (
    (NONE, "No experience in Chinese"),
    (SOME, "A few phrases here and there"),
    (SPEAK, "I can hold a decent conversation"),
    (FLUENT, "I'm fluent, but cannot read or write much"),
    (READANDWRITE, "I can read and write past an elementary level"),
)

# Gender
MALE = "M"
FEMALE = "F"
OTHER = "O"
PND = "P"
GENDER_CHOICES = (
    (MALE, "Male"),
    (FEMALE, "Female"),
    (OTHER, "Other"),
    (PND, "Prefer not to disclose"),
)


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.PositiveSmallIntegerField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    proficiency = models.PositiveSmallIntegerField(choices=PROFICIENCY_CHOICES)


class StudentHistory(models.Model):
    student = models.ForeignKey(Student)
    time = models.DateTimeField(auto_now_add=True)
