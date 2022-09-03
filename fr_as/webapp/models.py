from django.db import models
import os
# Create your models here.

def rename(instance, filename):
    main_dir = "student_faces"
    return os.path.join(main_dir, f"{instance}.jpg")

class student_face(models.Model):
    name = models.CharField(max_length=50)
    photo = models.ImageField(upload_to=rename)
    
    def __str__(self):
        return self.name
