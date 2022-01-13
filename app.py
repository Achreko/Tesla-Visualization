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
            print("\n\nDownloading data-----------\n\n")
            for id in range(1,7):
                (name, data) = get_new_data(id)
                # time.sleep(0.01)
                add_measurements(name, id, data)
            #expire_data(10)
            time.sleep(1)


if __name__ == "__main__":

    
    create_layout()
    
    collector = DataCollectorThread()
    collector.start()

    try:
        app.run_server(debug=True)
    finally:
        stop_collector = True
        collector.join()
        close_db_connection()
        print("Finished.")