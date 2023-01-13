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
    search_fields = ["name__name"]

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
                    
                    self.sendEmails[email][0].append(f'{record.name} : {time}')
    
    def getAbsentStudents(self):
        def create_record(obj):
            record = attendance()
            record.name = obj
            record.grade = obj.grade
            record.status = "A"
            record.datetime = self.datetoday
            record.save()
        
        for obj in students.objects.all():
            try:
                objs = attendance.objects.filter(name=obj)
                check = []
                for obj2 in objs:
                    if obj2.datetime.date() != self.datetoday:
                        check.append(True)
                    else:
                        check.append(False)
                if all(check):
                    create_record(obj)
            except:
                create_record(obj)
            
            if str(obj.name) not in self.nameList:
                email = self.getClassObj(obj.grade).form_teacher
                if email not in self.sendEmails.keys():
                    self.sendEmails[email] = [[],[]]
                self.sendEmails[email][1].append(f'{obj.name}')
    
    def send(self, request, queryset):
        self.initialize()
        for email_receiver in self.sendEmails.keys():
            grade = classes.objects.get(form_teacher=email_receiver).grade
            subject = f'{self.datetoday} {grade} Attendance'

            em = EmailMessage()
            em['From'] = self.email_sender
            em['To'] = email_receiver
            em['Subject'] = subject

            body1, body2 = "", ""

            count = 0
            for student in self.sendEmails[email_receiver][0]:
                count += 1
                body1 += str(count) + ". " + student + " "

            count = 0
            for student in self.sendEmails[email_receiver][1]:
                count += 1
                body2 += str(count) + ". " + student + " "

            em.add_alternative(f'''
            <img src="https://media-exp1.licdn.com/dms/image/C4E16AQF6N5Q-NKu9hg/profile-displaybackgroundimage-shrink_200_800/0/1615782069425?e=2147483647&v=beta&t=CMcupPyTebZ9wHQ51M9vq9a6YVMTSlwFrxnsoyfxpks" alt="Merlion School Header">
            <h1>{subject}</h1>
            <h2><u>Late Students</u></h2>
            <h3><i>{body1}</i></h3>
            <h2><u>Absent Students</u></h2>
            <h3><i>{body2}</i></h3>
            ''', subtype='html')

            self.smtp.sendmail(self.email_sender, email_receiver, em.as_string())

    changelist_actions = ['send']

class div_admin(admin.ModelAdmin):
    list_display = ["ay", "division"]

admin.site.register(students, stud_admin)
admin.site.register(attendance, aten_admin)
admin.site.register(division, div_admin)
admin.site.register([academic_year, classes])
