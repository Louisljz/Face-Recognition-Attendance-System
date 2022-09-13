from django.contrib import admin
from .models import *

# Register your models here.
# class att_admin(admin.ModelAdmin):
#     readonly_fields = ('date', 'name', 'time')
#     list_display = ('date', 'name', 'time')

class calen_admin(admin.ModelAdmin):
    readonly_fields = ('date', 'late_students')

class face_admin(admin.ModelAdmin):
    readonly_fields = ['presence', 'status' , 'image_tag']

class encod_admin(admin.ModelAdmin):
    readonly_fields = ['name', 'encoding1', 'encoding2', 'encoding3']


admin.site.register([Secondary_1, Secondary_2, Secondary_3, Secondary_4,
                    PreU_1, PreU_2], face_admin)
admin.site.register(face_encodings, encod_admin)
admin.site.register(calendar, calen_admin)

# admin.site.register(late_student, att_admin)