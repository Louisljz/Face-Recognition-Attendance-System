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
    
    def image_tag(self):
        return mark_safe('<img src="{}" width="150" height="150"/>'.format(self.photo1.url))

    image_tag.short_description = 'Image'

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
