from django.shortcuts import render
from django.contrib import messages
from fr_as.settings import MEDIA_ROOT
from .models import *
from datetime import date
import cv2
import face_recognition
import urllib
import numpy as np
import pickle
import base64


# Create your views here.
def img_to_encod(request, path, photo, url):
    resp = urllib.request.urlopen(url)
    arr = np.asarray(bytearray(resp.read()), dtype="uint8")
    img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    resized_img = imutils.resize(img, width=500)

    filepath = os.path.join(MEDIA_ROOT, str(path))
    cv2.imwrite(filepath, resized_img)

    encode = np.array([])
    faceEncodList = face_recognition.face_encodings(resized_img)

    if len(faceEncodList) == 0:
        messages.error(request, f'Cannot Find a Face in {photo}')
    elif len(faceEncodList) > 1:
        messages.error(request, f'Multiple Faces in {photo}')
    else:
        encode = faceEncodList[0]

    return encode


def convert(encod):
    if encod.size > 0:
        np_bytes = pickle.dumps(encod)
        np_base64 = base64.b64encode(np_bytes)
        return np_base64


def create_encodings(request):
    local_host = 'http://10.0.0.10:8000/'
    objects = student_profile.objects.all()
    if len(objects) > 0:
        for obj in objects:
            if obj.photo1:
                if not obj.encoding1:
                    photo = f'{obj.name}, Photo 1'
                    encod = img_to_encod(request, obj.photo1, photo, local_host+obj.photo1.url)
                    obj.encoding1 = convert(encod)
            else:
                obj.encoding1 = b''

            if obj.photo2:
                if not obj.encoding2:
                    photo = f'{obj.name}, Photo 2'
                    encod = img_to_encod(request, obj.photo2, photo, local_host+obj.photo2.url)
                    obj.encoding2 = convert(encod)
            else:
                obj.encoding2 = b''

            if obj.photo3:
                if not obj.encoding3:
                    photo = f'{obj.name}, Photo 3'
                    encod = img_to_encod(request, obj.photo3, photo, local_host+obj.photo3.url)
                    obj.encoding3 = convert(encod)
            else:
                obj.encoding3 = b''

            obj.save()

        messages.info(request, 'Attendance Sheet Created!')


def create_attendance():
    past_dates = []
    for obj in calendar.objects.all():
        past_dates.append(obj.date)
    
    if date.today() not in past_dates:
        new_date = calendar(date=date.today())
        new_date.save()
    
    attendance.objects.all().delete()
    profiles = student_profile.objects.all()
    for obj in profiles:
        student = attendance(name=obj, grade=obj.grade)
        student.save()


def home(request):
    return render(request, 'home.html')

def app(request):
    return render(request, 'app.html')

def stream(request):
    create_encodings(request)
    create_attendance()

    return render(request, 'stream.html')
