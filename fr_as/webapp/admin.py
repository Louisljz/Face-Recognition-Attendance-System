from django.contrib import admin
from django_object_actions import DjangoObjectActions
from .models import *
from .CreateEncods import CreateEncods


class stud_admin(DjangoObjectActions, admin.ModelAdmin):
    readonly_fields = ['image_tag']
    list_display = ['name', 'grade']
    ordering = ['name', 'grade']
    list_filter = ["grade"]

    def generate(modeladmin, request, queryset):
        encodings = CreateEncods()
        encodings.create_encodings(request)

    changelist_actions = ['generate']

class aten_admin(admin.ModelAdmin):
    list_display = ["name", "grade", "status", "datetime"]
    list_filter = ["grade", "status", "datetime"]

class div_admin(admin.ModelAdmin):
    list_display = ["ay", "division"]

admin.site.register(students, stud_admin)
admin.site.register(attendance, aten_admin)
admin.site.register(division, div_admin)
admin.site.register([academic_year, classes])
