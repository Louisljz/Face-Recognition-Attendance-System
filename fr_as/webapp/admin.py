from django.contrib import admin
from .models import *

# Register your models here.
class att_admin(admin.ModelAdmin):
    readonly_fields = ('name', 'time')
    list_display = ('name', 'time')

class face_admin(admin.ModelAdmin):
    readonly_fields = ['image_tag']
    list_display = ('name', 'image_tag')

admin.site.register(student_face, face_admin)
admin.site.register(attendance, att_admin)
admin.site.register([Secondary_1, Secondary_2, Secondary_3, Secondary_4,
                    PreU_1, PreU_2], face_admin)
