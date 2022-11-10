from django.db import models
from django.utils.html import mark_safe
import os
import urllib
import numpy as np
import cv2
import imutils
import face_recognition
from fr_as.settings import MEDIA_ROOT
# Create your models here.

class Rename:
    def __init__(self, number):
        self.number = number

    def save(self, instance, filename):
        instance = str(instance)
        alphabet = instance[0].upper()
        newpath = os.path.join(MEDIA_ROOT, alphabet)

        if not os.path.exists(newpath):
            os.makedirs(newpath)
        
        ext = os.path.splitext(filename)[1]
        filename = f"{instance}{self.number}{ext}"
        return os.path.join(newpath, filename)


class student_profile(models.Model):
    choices = (
            ('S1', 'Secondary_1'),
            ('S2', 'Secondary_2'),
            ('S3', 'Secondary_3'), 
            ('S4', 'Secondary_4'), 
            ('PU1', 'PreU_1'),
            ('PU2', 'PreU_2')
                                )
    name = models.CharField(max_length=50)
    grade = models.CharField(max_length=3, choices=choices)

    photo1 = models.ImageField(upload_to=Rename(1).save, max_length=500)
    photo2 = models.ImageField(upload_to=Rename(2).save, blank=True, max_length=500)
    photo3 = models.ImageField(upload_to=Rename(3).save, blank=True, max_length=500)
    
    encoding1 = models.BinaryField(blank=True, null=True, editable=False)
    encoding2 = models.BinaryField(blank=True, null=True, editable=False)
    encoding3 = models.BinaryField(blank=True, null=True, editable=False)

    photoUI = models.ImageField(editable=False, blank=True)

    def fetch_img(self):
        local_host = 'http://10.0.0.13:8000'
        image_url = local_host + self.photo1.url
        resp = urllib.request.urlopen(image_url)
        arr = np.asarray(bytearray(resp.read()), dtype="uint8")
        img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
        return img

    def set_filepath(self):
        path = os.path.join(MEDIA_ROOT, 'PhotoUI')
        filename = self.name + '_PhotoUI.jpg'
        filepath = os.path.join(path, filename)
        return filepath

    def insert_text(self, img, filepath, text):
        image = imutils.resize(img, width=200)
        cv2.putText(image,text,(0, int(image.shape[0]/2)),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),2)
        cv2.imwrite(filepath, image)
    
    def image_tag(self):
        if self.photo1:
            img = self.fetch_img()
            filepath = self.set_filepath()
            resized_img = imutils.resize(img, width=500)
            faceLocList = face_recognition.face_locations(resized_img)

            if len(faceLocList) == 1:
                faceLoc = faceLocList[0]
                y1,x2,y2,x1 = faceLoc
                cropped_img = resized_img[y1:y2, x1:x2]

                face_img = imutils.resize(cropped_img, width=200)
                cv2.imwrite(filepath, face_img)

            elif len(faceLocList) > 1:
                text = 'MANY FACES'
                self.insert_text(resized_img, filepath, text)
            
            else:
                text = 'NO FACE'
                self.insert_text(resized_img, filepath, text)

            self.photoUI = filepath
            self.save()

        return mark_safe('<img src="{}"/>'.format(self.photoUI.url))

    image_tag.short_description = 'Face'

    def save(self, *args, **kwargs):
        try:
            obj = student_profile.objects.get(pk=self.pk)
        except student_profile.DoesNotExist:
            pass 
        else:
            if not obj.photo1 == self.photo1: 
                self.encoding1 = b''
            if not obj.photo2 == self.photo2: 
                self.encoding2 = b''
            if not obj.photo3 == self.photo3: 
                self.encoding3 = b''
        super(student_profile, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class attendance(models.Model):
    name = models.ForeignKey(student_profile, on_delete=models.CASCADE)
    grade = models.CharField(max_length=3, blank=True, null=True)
    presence = models.BooleanField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)

    def __str__(self):
        return str(self.name)


class calendar(models.Model):
    date = models.DateField()
    late_students = models.ManyToManyField(student_profile)

    def get_students(self):
        return ", ".join([student.name for student in self.late_students.all()])

    get_students.short_description = 'Late Students'

    def __str__(self):
        return str(self.date)

