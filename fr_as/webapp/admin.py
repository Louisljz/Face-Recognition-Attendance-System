from django.contrib import admin
from django_object_actions import DjangoObjectActions
from .models import *
from .CreateEncods import CreateEncods
from datetime import datetime
import os
import smtplib
import ssl
from email.message import EmailMessage

class stud_admin(DjangoObjectActions, admin.ModelAdmin):
    readonly_fields = ['image_tag']
    list_display = ['name', 'grade']
    ordering = ['name', 'grade']
    list_filter = ["grade"]

    def generate(modeladmin, request, queryset):
        encodings = CreateEncods()
        encodings.create_encodings(request)

    changelist_actions = ['generate']

class aten_admin(DjangoObjectActions, admin.ModelAdmin):
    list_display = ["name", "grade", "status", "datetime"]
    list_filter = ["grade", "status", "datetime"]

    def initialize(self):
        self.choices = self.generate_choices()
        self.smtp, self.email_sender = self.initiate_email()
        self.datetoday = datetime.now().date()
        self.sendEmails = {}
        self.nameList = []

        self.getLateStudents()
        self.getAbsentStudents()

    def generate_choices(self):
        choices = []

        for i in range(1,7):
            choices.extend([("P"+str(i), "Primary "+str(i)),
                            ("P"+str(i)+"A", "Primary "+str(i)+"A"),
                            ("P"+str(i)+"B", "Primary "+str(i)+"B")])

        for i in range(1,5):
            choices.extend([("S"+str(i), "Secondary "+str(i))])

        for i in range(1,3):
            choices.extend([("PU"+str(i), "Pre-U "+str(i))])

        choices = tuple(choices)
        return choices

    def initiate_email(self):
        email_sender = 'louis.zhang@student.merlionis.sch.id'
        email_password = os.environ.get('Python Gmail Password')
        context = ssl.create_default_context()
        smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context)
        smtp.login(email_sender, email_password)
        return smtp, email_sender

    def getClassObj(self, value):
        for set in self.choices:
            if set[1] == str(value):
                grade = set[0]
                obj = classes.objects.get(grade=grade)
                break
        return obj

    def getLateStudents(self):
        records = attendance.objects.all()
        for record in records:
            if record.datetime.date() == self.datetoday and record.status != "A":
                self.nameList.append(str(record.name))
                obj = self.getClassObj(record.grade)

                email = obj.form_teacher
                
                if email not in self.sendEmails.keys():
                    self.sendEmails[email] = [[],[]]
                
                if record.status == "L":
                    time = record.datetime.strftime("%H:%M:%S")                
                    
                    self.sendEmails[email][0].append(f'{record.name} : {time}\n')
    
    def getAbsentStudents(self):
        for obj in students.objects.all():
            try:
                attendance.objects.get(name=obj)
            except:
                record = attendance()
                record.name = obj
                record.grade = obj.grade
                record.status = "A"
                record.datetime = self.datetoday
                record.save()

            if str(obj.name) not in self.nameList:
                email = self.getClassObj(obj.grade).form_teacher
                if email not in self.sendEmails.keys():
                    self.sendEmails[email] = [[],[]]
                self.sendEmails[email][1].append(f'{obj.name}\n')
    
    def send(self, request, queryset):
        self.initialize()
        for email_receiver in self.sendEmails.keys():
            grade = classes.objects.get(form_teacher=email_receiver).grade
            subject = f'{self.datetoday} {grade} Attendance'

            em = EmailMessage()
            em['From'] = self.email_sender
            em['To'] = email_receiver
            em['Subject'] = subject

            body = 'Late Students\n'
            for student in self.sendEmails[email_receiver][0]:
                body += student

            body += '\nAbsent Students:\n'
            for student in self.sendEmails[email_receiver][1]:
                body += student

            em.set_content(body)
            self.smtp.sendmail(self.email_sender, email_receiver, em.as_string())

    changelist_actions = ['send']

class div_admin(admin.ModelAdmin):
    list_display = ["ay", "division"]

admin.site.register(students, stud_admin)
admin.site.register(attendance, aten_admin)
admin.site.register(division, div_admin)
admin.site.register([academic_year, classes])
