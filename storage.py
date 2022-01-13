import time
import sqlite3

def init_storage():
    global _conn
    global _curs 
    _conn = sqlite3.connect('patients.db')
    _curs = _conn.cursor()
    _curs.execute("DROP TABLE IF EXISTS USERS")
    _conn.commit()
    return _conn

def get_curs():
    global _curs
    return _curs

def add_measurements(patient_name, patient_id, data):
    global _conn
    c = get_curs()
    c.execute("""CREATE TABLE IF NOT EXISTS USERS (
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
    



# def expire_data(secs):
#     c = get_curs()
#     for pid, pd in st.items():
#         print("\n\nClearing data ----------\n\n")
#         ts = time.time()
#         while len(pd["_expire_ts"]) > 0 and pd["_expire_ts"][0] < (ts-secs):
#             pd["datetimes"].pop(0)
#             pd["timestamps"].pop(0)
#             pd["values"].pop(0)
#             pd["anomalies"].pop(0)
#             pd["_expire_ts"].pop(0)

def close_db_connection():
    _conn.close()