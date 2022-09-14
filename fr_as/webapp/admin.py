from django.contrib import admin
from .models import *

class calen_admin(admin.ModelAdmin):
    readonly_fields = ['date', 'late_students']
    ordering = ['date']


class face_admin(admin.ModelAdmin):
    readonly_fields = ['presence', 'time', 'status', 'image_tag']
    list_filter = ['grade', 'presence', 'status']
    list_display = ['name', 'grade', 'presence', 'status']
    ordering = ['name']


class encod_admin(admin.ModelAdmin):
    readonly_fields = ['name', 'encoding1', 'encoding2', 'encoding3']


admin.site.register(student_profile, face_admin)
admin.site.register(face_encodings, encod_admin)
admin.site.register(calendar, calen_admin)
