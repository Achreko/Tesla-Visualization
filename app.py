from storage import *
import time
from apiclient import get_new_data
import threading
from dash_app import app, create_layout

stop_collector = False
class DataCollectorThread(threading.Thread):
    def run(self):
        init_storage()
        while(not stop_collector):
            for id in range(1,7):
                (name, data) = get_new_data(id)
                add_measurements(name, id, data)
            expire_data(600)
            time.sleep(1)
        close_db_connection()


if __name__ == "__main__":
    
    collector = DataCollectorThread()
    collector.start()

    create_layout()

    try:
        app.run_server(debug=True)
    finally:
        stop_collector = True
        collector.join()
        print("Finished.")