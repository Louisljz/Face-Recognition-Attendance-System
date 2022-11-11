import os
from pathlib import Path
import datetime
import sqlite3
import pickle
import base64


class TakeAttendance:
    def __init__(self):
        self.late = datetime.time(7, 30, 0)
        self.datetoday = datetime.datetime.now().date()

        self.db_conn = self.create_connection()
        self.fetch_encods()
        self.nameList = self.getNameList()
        
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
        SELECT * FROM webapp_students
        ''')
        record_list = result.fetchall()

        self.classNames = []
        self.encodeListKnown = []

        for i in range(len(record_list)):
            obj = self.db_conn.execute('''
            SELECT grade FROM webapp_classes
            WHERE id = (?)
            ''', (record_list[i][9], ))
            self.label = record_list[i][1] + f' ({obj.fetchone()[0]})'
            
            encoding1 = record_list[i][5]
            encoding2 = record_list[i][5]
            encoding3 = record_list[i][7]

            if encoding1:
                self.convert(encoding1)

            if encoding2:
                self.convert(encoding2)

            if encoding3:
                self.convert(encoding3)
    
    def getNameList(self):
        nameList = []

        obj = self.db_conn.execute(r'''
        SELECT * FROM webapp_attendance
        WHERE DATE(datetime) = (?)
        ''', (self.datetoday, ))

        result = obj.fetchall()

        if result:
            for record in result:
                nameid = record[4]
                obj2 = self.db_conn.execute('''
                                            SELECT name FROM webapp_students
                                            WHERE id = (?)
                                            ''', (nameid, ))

                name = obj2.fetchone()[0]

                nameList.append(name)
            
        return nameList

    def markAttendance(self, name):
        if name not in self.nameList:
            self.nameList.append(name)
            current = datetime.datetime.now()

            obj = self.db_conn.execute('''
            SELECT id, grade_id FROM webapp_students
            WHERE name = (?)
            ''', (name, ))

            name_grade = obj.fetchone()

            if current.time() > self.late:
                self.db_conn.execute('''
                            INSERT INTO webapp_attendance (status, datetime, grade_id, name_id)
                                        VALUES ("L", ?, ?, ?)
                            ''', (current, name_grade[1], name_grade[0]))
            
            else:
                self.db_conn.execute('''
                            INSERT INTO webapp_attendance (status, datetime, grade_id, name_id)
                                        VALUES ("P", ?, ?, ?)
                            ''', (current, name_grade[1], name_grade[0]))
            self.db_conn.commit()
