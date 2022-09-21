from pathlib import Path
import os
import sqlite3
import pickle
import base64

# Create your tests here.

BASE_DIR = Path(__file__).resolve().parent.parent
database = os.path.join(BASE_DIR, 'db.sqlite3')

def create_connection(database):
    try:
        conn = sqlite3.connect(database)
        return conn
    except:
        print("Unable to connect to DB")

# Connect to the database
db_conn = create_connection(database)


# result = db_conn.execute('''
# SELECT * FROM webapp_attendance
# ''')
# record_list = result.fetchall()

# name = db_conn.execute('''
# SELECT name FROM webapp_student_profile
# WHERE id = (?)
# ''', (record_list[0][4], ))

# print('NAME:', name.fetchone()[0] + f' ({record_list[0][1]})')
# print('PRESENCE:', record_list[0][2])

# import datetime

# current = datetime.datetime.now().time()
# late = datetime.time(7, 30, 0)

# if current > late:
#     print("LATE")

# time_str = current.strftime('%H:%M')
# print(time_str)

# text = 'Louis (S4)'

# print(text.split()[0])
# print(text.split()[1][1:-1])

# label = 'Louis J.Zhang (S4)'

# obj = db_conn.execute('''
# SELECT id FROM webapp_student_profile
# WHERE name = (?) AND grade = (?)
# ''', (label.split('(')[0].strip(), label.split('(')[1][:-1]))

# print(obj.fetchone()[0])

# import datetime

# date_today = datetime.datetime.now().date()
# print(date_today)

# obj = db_conn.execute('''
# SELECT id FROM webapp_calendar
# WHERE date = (?)
# ''', (date_today, ))

# print(obj.fetchone()[0])

# result = db_conn.execute('''
# SELECT encoding1 FROM webapp_student_profile
# ''')
# record_list = result.fetchall()

# binary = record_list[0][0]

# np_bytes = base64.b64decode(binary)

# np_array = pickle.loads(np_bytes)

# print(len(record_list))
# print(type(np_array))
# print(np_array)

# byte = b''

# if byte:
#     print('yes')

# from pathlib import Path

# BASE_DIR = Path(__file__).resolve().parent.parent
# MEDIA_ROOT = os.path.join(BASE_DIR, "aten_monitor/student_faces")

# newpath = os.path.join(MEDIA_ROOT, 'c/')

# if not os.path.exists(newpath):
#     print("hi")
#     os.makedirs(newpath)

# print(newpath)

# text = 'louis'
# print(text[0])

# import pickle
# import base64
# import numpy as np

# encode = None

# np_bytes = pickle.dumps(encode)
# np_base64 = base64.b64encode(np_bytes)

# if np_base64:
#     print(encode)
#     print(np_base64)
#     np_bytes = base64.b64decode(np_base64)
#     np_array = pickle.loads(np_bytes)
#     print(np_array)

# state = None

# state = 'hi'

# print(state)

# import numpy as np

# x = np.array([])

# if x.size > 0:
#     print('hi')
