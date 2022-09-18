from django.contrib import admin, messages
from .models import *
import cv2
import face_recognition
import urllib
import numpy as np
import pickle
import base64


def img_to_encod(url):
    resp = urllib.request.urlopen(url)
    arr = np.asarray(bytearray(resp.read()), dtype="uint8")
    img = cv2.imdecode(arr, -1)
    encode = face_recognition.face_encodings(img)[0]
    return encode

@admin.action(description='Generate Face Encodings')
def generate_encod(modeladmin, request, queryset):
    local_host = 'http://127.0.0.1:8000/'

    for obj in queryset:
        if obj.photo1:
            encod = img_to_encod(local_host+obj.photo1.url)
            np_bytes = pickle.dumps(encod)
            np_base64 = base64.b64encode(np_bytes)
            obj.encoding1 = np_base64
            obj.save()

        if obj.photo2:
            encod = img_to_encod(local_host+obj.photo2.url)
            np_bytes = pickle.dumps(encod)
            np_base64 = base64.b64encode(np_bytes)
            obj.encoding2 = np_base64
            obj.save()
            
        if obj.photo3:
            encod = img_to_encod(local_host+obj.photo3.url)
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


class atten_admin(admin.ModelAdmin):
    readonly_fields = ['presence', 'time', 'grade']
    list_filter = ['presence', 'grade']
    list_display = ['name', 'grade', 'presence']
    ordering = ['name', 'grade']


class calen_admin(admin.ModelAdmin):
    # readonly_fields = ['date', 'late_students']
    list_display = ['date', 'get_students']
    ordering = ['date']


admin.site.register(student_profile, stud_admin)
admin.site.register(attendance, atten_admin)
admin.site.register(calendar, calen_admin)
