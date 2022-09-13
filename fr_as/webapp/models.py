from django.db import models
from django.utils.html import mark_safe
import os
# Create your models here.

class Rename:
    def __init__(self, number):
        self.number = number

    def save(self, instance, filename):
        ext = os.path.splitext(filename)[1]
        return f"{instance}{self.number}{ext}"


class student_face(models.Model):
    name = models.CharField(max_length=50)
    presence = models.BooleanField(default=False)
    status = models.BooleanField(blank=True, null=True)

    photo1 = models.ImageField(upload_to=Rename(1).save)
    photo2 = models.ImageField(upload_to=Rename(2).save, blank=True)
    photo3 = models.ImageField(upload_to=Rename(3).save, blank=True)
    
    def image_tag(self):
        return mark_safe('<img src="{}" width="150" height="150"/>'.format(self.photo1.url))

    image_tag.short_description = 'Image'

    def __str__(self):
        return self.name


class Secondary_1(student_face):
    pass

class Secondary_2(student_face):
    pass

class Secondary_3(student_face):
    pass

class Secondary_4(student_face):
    pass

class PreU_1(student_face):
    pass

class PreU_2(student_face):
    pass


class face_encodings(models.Model):
    name = models.CharField(max_length=50)
    encoding1 = models.BinaryField()
    encoding2 = models.BinaryField(blank=True)
    encoding3 = models.BinaryField(blank=True)

    def __str__(self):
        return self.name


class calendar(models.Model):
    date = models.DateField()
    late_students = models.TextField()

    def __str__(self):
        return str(self.date)

# class late_student(models.Model):
#     date = models.ForeignKey(calendar, on_delete=models.CASCADE)
#     name = models.CharField(max_length=50)
#     time = models.TimeField()

#     def __str__(self):
#         return self.name

