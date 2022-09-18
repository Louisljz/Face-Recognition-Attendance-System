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

result = db_conn.execute('''
SELECT encoding1 FROM webapp_student_profile
''')
record_list = result.fetchall()

binary = record_list[0][0]

np_bytes = base64.b64decode(binary)

np_array = pickle.loads(np_bytes)

print(len(record_list))
print(type(np_array))
print(np_array)
