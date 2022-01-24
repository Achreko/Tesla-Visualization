import time
import sqlite3

def init_storage():
    global _conn
    global _curs 
    _conn = sqlite3.connect('patients.db')
    _curs = _conn.cursor()
    _curs.execute("DROP TABLE IF EXISTS USERS")
    _curs.execute("""CREATE TABLE IF NOT EXISTS USERS (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        patient_id integer,
        patient_name text,
        datetimes text,
        timestamps text,
        val text,
        anomalies text,
        end_time text
    );
    """)
    _conn.commit()
    return _conn

def get_curs():
    global _curs
    return _curs

def add_measurements(patient_name, patient_id, data):
    global _conn
    c = get_curs()
    if not is_in_db(patient_id, data["timestamp"]):
        c.execute(f"""INSERT INTO USERS VALUES(
            null,
            {patient_id}, 
            '{patient_name}',
            '{data['datetime']}',
            '{data['timestamp']}',
            '{data['values']}',
            '{data['anomalies']}',
            '{time.time()}'
        );""")
        _conn.commit()

def expire_data(secs):
    c = get_curs()
    ts = time.time()
    c.execute("DELETE FROM USERS WHERE end_time<?", (ts-secs,))
    _conn.commit()

def is_in_db(patient_id, timestamp):
    c = get_curs()
    c.execute("SELECT * FROM USERS WHERE patient_id=? AND timestamps=?", (patient_id, timestamp,))
    row = c.fetchone()
    return False if row is None else True
    
def convert_data_to_df(users):
    pd = {
             "patient_id": users[0][1],
             "patient_name": users[0][2],
             "datetimes": [],
             "timestamps": [],
             "values": [],
             "anomalies": [],
             "_expire_ts": []
         }
    for user in users:
        pd["datetimes"].append(user[3])
        pd["timestamps"].append(user[4])
        pd["values"].append(list(map(float,user[5][1:-1].split(', '))))
        pd["anomalies"].append(user[6][1:-1].split(', '))
        pd["_expire_ts"].append(user[7])
    return pd


def close_db_connection():
    _conn.close()