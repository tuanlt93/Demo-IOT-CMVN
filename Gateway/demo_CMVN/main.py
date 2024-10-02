from flask import Flask, jsonify
from flask_cors import CORS
import threading
import time
from util.influx_database import writeData, queryData
from util.time_converter import dateTime2Epoch
from util.comiunity_plc import PLCStation
from datetime import datetime
import redis

redis_client = redis.Redis(host='localhost', port=6379, db=0)

app = Flask(__name__)
CORS(app)  # Bật CORS cho toàn bộ ứng dụng Flask

def readDataPlc():
    while True:
        try:
            comiunity_PLC = PLCStation()
            data_register = comiunity_PLC.read_registers()
            redis_client.set("error", data_register[12])
            data_coil = comiunity_PLC.read_coil()
            writeData(machine_model= 123456,
                      current_status= int(data_coil),
                      product_count= int(data_register[6]),
                      running_time= int(data_register[8]),
                      power_on_time= int(data_register[10])
                      )
        except Exception as e:
            print(f"Error reading PLC data: {e}")
        time.sleep(30)


@app.route('/machine/data', methods=['GET'])
def readData():
    try:
        time_now = datetime.now()
        start_of_day = time_now.replace(hour=0, minute=0, second=0, microsecond=0)

        time_start = dateTime2Epoch(start_of_day)
        time_end = dateTime2Epoch(time_now)
        
        error_id = redis_client.get("error")
        if error_id is None:
            error_id = "0"
        else:
            error_id = error_id.decode('utf-8')

        quantity, number_idle, running_time, power_on_time = queryData(time_start=time_start, time_stop=time_end, machine_model=123456)

        data_response = {
            "quantity": quantity,
            "number_idle": number_idle,
            "running_time": running_time,
            "power_on_time": power_on_time,
            "error": int(error_id)
        }
        return jsonify(data_response)

    except Exception as e:
        data_response1 = {
            "quantity": quantity,
            "number_idle": number_idle,
            "running_time": running_time,
            "power_on_time": power_on_time,
            "error": 11311
        }
        return jsonify(data_response1)


if __name__ == '__main__':
    threading.Thread(target=readDataPlc, daemon= True).start()
    app.run(host="0.0.0.0", port=5001)
