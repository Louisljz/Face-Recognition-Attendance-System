from django.contrib import admin
from .models import student_face, attendance

# Register your models here.
class att_admin(admin.ModelAdmin):
    readonly_fields = ('name', 'time')

class face_admin(admin.ModelAdmin):
    readonly_fields = ['image_tag']

admin.site.register(student_face, face_admin)
admin.site.register(attendance, att_admin)
