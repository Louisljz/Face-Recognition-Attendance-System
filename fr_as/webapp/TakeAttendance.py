import os
from pathlib import Path
import datetime
import sqlite3
import pickle
import base64


class TakeAttendance:
    def __init__(self):
        self.db_conn = self.create_connection()
        self.fetch_encods()
        self.nameList = self.getNameList()
        self.late = datetime.time(7, 30, 0)
        self.date_today = datetime.datetime.now().date()

    def create_connection(self):
        BASE_DIR = Path(__file__).resolve().parent.parent
        database = os.path.join(BASE_DIR, "db.sqlite3")
        try:
            conn = sqlite3.connect(database)
            return conn
        except:
            print("Unable to connect to DB")

    def convert(self, encoding):
        np_bytes = base64.b64decode(encoding)
        np_array = pickle.loads(np_bytes)
        self.encodeListKnown.append(np_array)
        self.classNames.append(self.label)

    def fetch_encods(self):
        result = self.db_conn.execute('''
        SELECT * FROM webapp_student_profile
        ''')
        record_list = result.fetchall()

        self.classNames = []
        self.encodeListKnown = []

        for i in range(len(record_list)):
            self.label = record_list[i][1] + f' ({record_list[i][2]})'
            
            encoding1 = record_list[i][6]
            encoding2 = record_list[i][7]
            encoding3 = record_list[i][8]

            if encoding1:
                self.convert(encoding1)

            if encoding2:
                self.convert(encoding2)

            if encoding3:
                self.convert(encoding3)
    
    def getNameList(self):
        nameList = []
        result = self.db_conn.execute('''
        SELECT * FROM webapp_attendance
        ''')
        record_list = result.fetchall()

        for i in range(len(record_list)):
            presence = record_list[i][2]

            if presence != None:
                obj = self.db_conn.execute('''
                SELECT name FROM webapp_student_profile
                WHERE id = (?)
                ''', (record_list[i][4], ))

                name = obj.fetchone()[0]

                nameList.append(name)
        
        return nameList

    def markAttendance(self, name, grade):
        if name not in self.nameList:
            self.nameList.append(name)
            
            current = datetime.datetime.now().time()
            time_str = current.strftime('%H:%M')

            obj = self.db_conn.execute('''
            SELECT id FROM webapp_student_profile
            WHERE name = (?) AND grade = (?)
            ''', (name, grade))

            id = obj.fetchone()[0]

            self.db_conn.execute('''
                            UPDATE webapp_attendance
                            SET time = (?)
                            WHERE name_id = (?)
                            ''', (time_str, id))
            self.db_conn.commit()

            if current > self.late:
                presence = False
                self.db_conn.execute('''
                            UPDATE webapp_attendance
                            SET presence = (?)
                            WHERE name_id = (?)
                            ''', (False, id))
                
                obj = self.db_conn.execute('''
                            SELECT id FROM webapp_calendar
                            WHERE date = (?)
                            ''', (self.date_today, ))

                cal_id = obj.fetchone()[0]

                self.db_conn.execute('''
                            INSERT INTO webapp_calendar_late_students (calendar_id, student_profile_id)
                            VALUES (?, ?)
                            ''', (cal_id, id))
                
                self.db_conn.commit()
            
            else:
                presence = True
                self.db_conn.execute('''
                            UPDATE webapp_attendance
                            SET presence = (?)
                            WHERE name_id = (?)
                            ''', (True, id))
                self.db_conn.commit()

            return time_str, presence

