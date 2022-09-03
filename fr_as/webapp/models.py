from django.db import models
import os
# Create your models here.

def rename(instance, filename):
    main_dir = "student_faces"
    ext = os.path.splitext(filename)[1]
    return os.path.join(main_dir, f"{instance}{ext}")

class student_face(models.Model):
    name = models.CharField(max_length=50)
    photo = models.ImageField(upload_to=rename)
    
    def __str__(self):
        return self.name


class attendance(models.Model):
    name = models.CharField(max_length=50)
    time = models.TimeField()

    def __str__(self):
        return self.name

