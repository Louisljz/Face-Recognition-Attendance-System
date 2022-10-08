from datetime import date
from django.shortcuts import render
from .models import *
from .CreateEncods import CreateEncods


def create_attendance():
    past_dates = []
    for obj in calendar.objects.all():
        past_dates.append(obj.date)
    
    if date.today() not in past_dates:
        new_date = calendar(date=date.today())
        new_date.save()
    
        attendance.objects.all().delete()
        profiles = student_profile.objects.all()
        for obj in profiles:
            student = attendance(name=obj, grade=obj.grade)
            student.save()


def home(request):
    return render(request, 'home.html')

def app(request):
    return render(request, 'app.html')

def stream(request):
    encodings = CreateEncods()
    encodings.create_encodings(request)
    create_attendance()
    if not encodings.error_message:
        pass

    return render(request, 'stream.html')
