from django.contrib import admin
from django_object_actions import DjangoObjectActions
from .models import *
from .CreateEncods import CreateEncods


class stud_admin(DjangoObjectActions, admin.ModelAdmin):
    readonly_fields = ['image_tag']
    list_display = ['name', 'grade']
    ordering = ['name', 'grade']

    def generate(modeladmin, request, queryset):
        encodings = CreateEncods()
        encodings.create_encodings(request)

    changelist_actions = ['generate']

admin.site.register(students, stud_admin)
admin.site.register([academic_year, division, classes, attendance])
