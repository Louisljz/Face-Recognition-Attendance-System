from django.contrib import admin
from .models import student_face, attendance

# Register your models here.
admin.site.register([student_face, attendance])