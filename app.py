from storage import *
import time
from apiclient import get_new_data
import threading
from dash_app import app, create_layout

stop_collector = False
class DataCollectorThread(threading.Thread):
    def run(self):
        while(not stop_collector):
            for id in range(1,7):
                (name, data) = get_new_data(id)
                add_measurements(name, id, data)
            expire_data(20)
            print(get_storage())
            time.sleep(1)


if __name__ == "__main__":

    init_storage()
    create_layout()
    
    collector = DataCollectorThread()
    collector.start()

    try:
        app.run_server(debug=True)
    finally:
        stop_collector = True
        collector.join()
        print("Finished.")