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


class atten_admin(admin.ModelAdmin):
    list_filter = ['presence', 'grade']
    list_display = ['name', 'grade', 'presence', 'time']
    ordering = ['name', 'grade']

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


class calen_admin(DjangoObjectActions, admin.ModelAdmin):
    list_display = ['date', 'get_students']
    ordering = ['-date']

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


admin.site.register(student_profile, stud_admin)
admin.site.register(attendance, atten_admin)
admin.site.register(calendar, calen_admin)
