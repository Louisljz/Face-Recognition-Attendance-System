from django.contrib import admin
from .models import student_face, attendance

# Register your models here.
class ItemAdmin(admin.ModelAdmin):
    readonly_fields = ('name', 'time')

admin.site.register(student_face)
admin.site.register(attendance, ItemAdmin)