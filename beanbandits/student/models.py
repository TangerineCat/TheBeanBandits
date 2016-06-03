from __future__ import unicode_literals

# Models the Student

from django.db import models
from django.contrib.auth.models import User
from .choices import *
# Create your models here.

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.PositiveSmallIntegerField(null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    proficiency = models.PositiveSmallIntegerField(choices=PROFICIENCY_CHOICES)

    def __unicode__(self):
        return '%s' % (self.user)


class StudentHistory(models.Model):
    student = models.ForeignKey(Student)
    time = models.DateTimeField(auto_now_add=True)
    finishtime = models.DateTimeField(null=True)
    score = models.PositiveIntegerField(null=True)

from registration.signals import user_registered

def user_registered_callback(sender, user, request, **kwargs):
    user = request.user
    user.first_name = unicode(request.POST["first_name"])
    user.save()
    student = Student(user=user)
    student.proficiency = request.POST["proficiency"]
    student.gender = request.POST["gender"]
    if "age" in request.POST:
        student.age = request.POST["age"]
    student.save()

user_registered.connect(user_registered_callback)