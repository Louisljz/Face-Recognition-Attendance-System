from datetime import date
from django.contrib import admin, messages
from django_object_actions import DjangoObjectActions
from .models import *
import cv2
import face_recognition
import urllib
import numpy as np
import pickle
import base64


def img_to_encod(request, photo, url):
    resp = urllib.request.urlopen(url)
    arr = np.asarray(bytearray(resp.read()), dtype="uint8")
    img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    resized_img = imutils.resize(img, width=500)

    encode = np.array([])
    faceEncodList = face_recognition.face_encodings(resized_img)

    if len(faceEncodList) == 0:
        messages.error(request, f'Cannot Find a Face in {photo}')
    elif len(faceEncodList) > 1:
        messages.error(request, f'Multiple Faces in {photo}')
    else:
        encode = faceEncodList[0]

    return encode


@admin.action(description='Generate Face Encodings')
def generate_encod(modeladmin, request, queryset):
    local_host = 'http://10.0.0.24:8000/'

    for obj in queryset:
        if obj.photo1:
            photo = f'{obj.name}, Photo 1'
            encod = img_to_encod(request, photo, local_host+obj.photo1.url)
            if encod.size > 0:
                np_bytes = pickle.dumps(encod)
                np_base64 = base64.b64encode(np_bytes)
                obj.encoding1 = np_base64
                obj.save()

        if obj.photo2:
            photo = f'{obj.name}, Photo 2'
            encod = img_to_encod(request, photo, local_host+obj.photo2.url)
            if encod.size > 0:
                np_bytes = pickle.dumps(encod)
                np_base64 = base64.b64encode(np_bytes)
                obj.encoding2 = np_base64
                obj.save()
            
        if obj.photo3:
            photo = f'{obj.name}, Photo 3'
            encod = img_to_encod(request, photo, local_host+obj.photo3.url)
            if encod.size > 0:
                np_bytes = pickle.dumps(encod)
                np_base64 = base64.b64encode(np_bytes)
                obj.encoding3 = np_base64
                obj.save()

    messages.info(request, 'Encodings have been generated!')


class stud_admin(admin.ModelAdmin):
    readonly_fields = ['image_tag']
    list_display = ['name', 'grade']
    ordering = ['name', 'grade']
    actions = [generate_encod]


class atten_admin(DjangoObjectActions, admin.ModelAdmin):
    list_filter = ['presence', 'grade']
    list_display = ['name', 'grade', 'presence', 'time']
    ordering = ['name', 'grade']

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def create(modeladmin, request, queryset):
        attendance.objects.all().delete()
        profiles = student_profile.objects.all()
        for obj in profiles:
            student = attendance(name=obj, grade=obj.grade)
            student.save()

    changelist_actions = ['create']


class calen_admin(DjangoObjectActions, admin.ModelAdmin):
    list_display = ['date', 'get_students']
    ordering = ['-date']

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def create(modeladmin, request, queryset):
        past_dates = []
        for obj in calendar.objects.all():
            past_dates.append(obj.date)

        if date.today() not in past_dates:
            new_date = calendar(date=date.today())
            new_date.save()

    changelist_actions = ['create']


admin.site.register(student_profile, stud_admin)
admin.site.register(attendance, atten_admin)
admin.site.register(calendar, calen_admin)
