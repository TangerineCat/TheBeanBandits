from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import Student, StudentHistory
# Create your views here.

@login_required()
def me(request):
    user = request.user
    me = Student.objects.filter(user=user).get()
    history = StudentHistory.objects.filter(student=me).order_by('finishtime')
    context = {
        'user': user,
        'me' : me,
    }
    return render(request, 'me.html', context)
