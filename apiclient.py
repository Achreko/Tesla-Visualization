import requests
from datetime import datetime

def get_new_data(patient_id):
    res = requests.get(f"http://tesla.iem.pw.edu.pl:9080/v2/monitor/{patient_id}")
    js = res.json()

    name = js["firstname"] + " " + js["lastname"]

    return name, {
        "datetime": change_timestamp_to_datetime(js["trace"]["id"]),
        "timestamp": js["trace"]["id"],
        "values": [ x["value"] for x in js["trace"]["sensors"] ],
        "anomalies": [ x["anomaly"] for x in js["trace"]["sensors"] ]
    }

def change_timestamp_to_datetime(timestamp):
    timestamp = str(timestamp)
    date = datetime(
    int(timestamp[-4:]),
    int(timestamp[-6:-4]),
    int(timestamp[-8:-6]),
    int(timestamp[:-12]),
    int(timestamp[-12:-10]),
    int(timestamp[-10:-8])
    )
    return date