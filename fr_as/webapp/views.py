from datetime import date
from django.shortcuts import render, redirect
from .models import *
from .CreateEncods import CreateEncods
from .aten_monitor import aten_monitor
from django.contrib import messages


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
    if request.user_agent.is_pc:
        return render(request, 'home.html')
    else:
        return redirect('admin:index')

def app(request):
    if request.user_agent.is_pc:
        return render(request, 'app.html')
    else:
        return redirect('admin:index')

def stream(request):
    if request.user_agent.is_pc:
        profiles = student_profile.objects.all()
        if len(profiles) > 0:
            encodings = CreateEncods()
            encodings.create_encodings(request)
            create_attendance()
            if not encodings.error_message:
                monitoring = aten_monitor()
                monitoring.start()
        else:
            messages.warning(request, 'Please Create At Least One Student Profile Before Continuing!')
        
        return render(request, 'stream.html')
    else:
        return redirect('admin:index')
