import cv2
import face_recognition
import numpy as np
from .TakeAttendance import TakeAttendance


class aten_monitor(TakeAttendance):
    def __init__(self):
        self.cap = cv2.VideoCapture(0)

    def start(self):
        while True:
            _, img = self.cap.read()

            imgS = cv2.resize(img,(0,0),None,0.25,0.25)
            imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
            
            facesCurFrame = face_recognition.face_locations(imgS)
            encodesCurFrame = face_recognition.face_encodings(imgS,facesCurFrame)
            
            for encodeFace,faceLoc in zip(encodesCurFrame,facesCurFrame):
                matches = face_recognition.compare_faces(self.encodeListKnown,encodeFace)
                faceDis = face_recognition.face_distance(self.encodeListKnown,encodeFace)

                matchIndex = np.argmin(faceDis)
                
                if faceDis[matchIndex] < 0.50:
                    name = self.classNames[matchIndex]
                    self.markAttendance(name)
                else: 
                    name = 'Unknown'
                
                y1,x2,y2,x1 = faceLoc
                y1, x2, y2, x1 = y1*4,x2*4,y2*4,x1*4
                cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
                cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
                cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
            
            cv2.imshow('Webcam',img)
            if cv2.waitKey(1) &0xFF == ord(' '):
                break

        self.cap.release()
        cv2.destroyAllWindows()
