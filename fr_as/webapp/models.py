from unicodedata import name
from django.db import models
from django.utils.html import mark_safe
from django.db.models.signals import post_save
from django.dispatch import receiver
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

    photo1 = models.ImageField(upload_to=Rename(1).save)
    photo2 = models.ImageField(upload_to=Rename(2).save, blank=True)
    photo3 = models.ImageField(upload_to=Rename(3).save, blank=True)
    
    encoding1 = models.BinaryField(editable=False)
    encoding2 = models.BinaryField(blank=True, editable=False)
    encoding3 = models.BinaryField(blank=True, editable=False)

    status = models.BooleanField(default=False)

    photoUI = models.ImageField(editable=False, blank=True)
    
    def image_tag(self):
        if self.photo1:
            local_host = 'http://127.0.0.1:8000/'
            image_url = local_host + self.photo1.url
            resp = urllib.request.urlopen(image_url)
            arr = np.asarray(bytearray(resp.read()), dtype="uint8")
            img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
            resized_img = imutils.resize(img, width=500)

            path = os.path.join(MEDIA_ROOT, 'PhotoUI')
            filename = self.name + '_PhotoUI.jpg'
            filepath = os.path.join(path, filename)

            faceLocList = face_recognition.face_locations(resized_img)

            if len(faceLocList) == 1:
                faceLoc = faceLocList[0]
                y1,x2,y2,x1 = faceLoc
                cropped_img = resized_img[y1:y2, x1:x2]

                face_img = imutils.resize(cropped_img, width=200)
                cv2.imwrite(filepath, face_img)
            else:
                noface_img = imutils.resize(resized_img, width=200)
                cv2.putText(noface_img,'NO FACE',(0, int(noface_img.shape[0]/2)),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),2)
                cv2.imwrite(filepath, noface_img)

            self.photoUI = filepath
            self.save()

        return mark_safe('<img src="{}"/>'.format(self.photoUI.url))

    image_tag.short_description = 'Face'

    def __str__(self):
        return self.name


@receiver(post_save, sender=student_profile)
def save_func(sender, instance, **kwargs):
    status = True
    if instance.photo1 and not instance.encoding1:
        status = False
    if instance.photo2 and not instance.encoding2:
        status = False
    if instance.photo3 and not instance.encoding3:
        status = False

    sender.objects.filter(name=instance.name).update(status=status)

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
