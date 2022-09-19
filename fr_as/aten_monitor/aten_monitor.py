import cv2
import numpy as np
import face_recognition
import os
from pathlib import Path
from datetime import datetime
import sqlite3
import pickle
import base64


BASE_DIR = Path(__file__).resolve().parent.parent

database = os.path.join(BASE_DIR, "db.sqlite3")

def create_connection(database):
    try:
        conn = sqlite3.connect(database)
        return conn
    except:
        print("Unable to connect to DB")

db_conn = create_connection(database)

result = db_conn.execute('''
SELECT * FROM webapp_student_profile
''')
record_list = result.fetchall()

classNames = []
encodeListKnown = []

for i in range(len(record_list)):
    label = record_list[i][1] + f' ({record_list[i][2]})'
    
    encoding1 = record_list[i][6]
    encoding2 = record_list[i][7]
    encoding3 = record_list[i][8]

    if encoding1:
        encodeListKnown.append(encoding1)
        classNames.append(label)
    if encoding2:
        encodeListKnown.append(encoding2)
        classNames.append(label)
    if encoding3:
        encodeListKnown.append(encoding3)
        classNames.append(label)

print(list(set(classNames)))
print(len(classNames))
print(len(encodeListKnown))

# CONTINUE FROM HERE
# def markAttendance(name):
#     result = db_conn.execute('''
#     SELECT * FROM webapp_attendance
#     ''')
#     record_list = result.fetchall()
#     nameList = []

#     for record in record_list:
#         nameList.append(record[1])
    
#     if name not in nameList:
#         now = datetime.now()
#         dtString = now.strftime('%H:%M:%S')
#         db_conn.execute('''
#                         INSERT INTO webapp_attendance (name, time)
#                         VALUES (?, ?)
#                         ''', (name, dtString))
#         db_conn.commit()


# cap = cv2.VideoCapture(0)

# while True:
#     success, img = cap.read()

#     imgS = cv2.resize(img,(0,0),None,0.25,0.25)
#     imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
    
#     facesCurFrame = face_recognition.face_locations(imgS)
#     encodesCurFrame = face_recognition.face_encodings(imgS,facesCurFrame)
    
#     for encodeFace,faceLoc in zip(encodesCurFrame,facesCurFrame):
#         matches = face_recognition.compare_faces(encodeListKnown,encodeFace)
#         faceDis = face_recognition.face_distance(encodeListKnown,encodeFace)

#         matchIndex = np.argmin(faceDis)
        
#         if faceDis[matchIndex] < 0.50:
#             name = classNames[matchIndex]
#             markAttendance(name)
#         else: 
#             name = 'Unknown'
        
#         y1,x2,y2,x1 = faceLoc
#         y1, x2, y2, x1 = y1*4,x2*4,y2*4,x1*4
#         cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
#         cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
#         cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
    
#     cv2.imshow('Webcam',img)
#     if cv2.waitKey(1) &0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()
