from flask import Flask, jsonify
from flask_cors import CORS
import threading
import time
import redis
from util.comiunity_plc import PLCStation
import csv
import datetime
from datetime import datetime, timezone

comiunity_PLC = PLCStation(serial_port="COM3", baudrate=9600, timeout=1)
redis_client = redis.StrictRedis(host="localhost", port=6379, decode_responses=True)

app = Flask(__name__)
CORS(app)  # Bật CORS cho toàn bộ ứng dụng Flask


csv_file = 'D:\data_demo.csv'

def readDataPlc():
    while True:
        data_register = comiunity_PLC.read_registers()
        if data_register:
            redis_client.set('data_register', str(data_register))
        else: data_register  = [0]* 13
        
        data_coil = comiunity_PLC.read_coil()
        if data_coil is not None:
            redis_client.set('data_coil', str(int(data_coil)))

        now_utc = str(datetime.now())
        
        
        with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            data_to_write = [
            [now_utc, data_register[6], data_register[8], data_register[10], data_register[12]]
            ]
            
            writer.writerows(data_to_write)
            file.flush()
            
            print(f'Đã ghi dữ liệu mới vào file {csv_file}')

        time.sleep(5)  




@app.route('/machine/data', methods=['GET'])
def readData():
    data_register = redis_client.get('data_register')
    data_coil = redis_client.get('data_coil')
    
    if not data_register:
        data_register = [0] * 13  
    else:
        data_register = eval(data_register)
    
    if not data_coil:
        data_coil = "False"
    else:
        data_coil = bool(int(data_coil))
    
    data_response = {
        "machine_model": data_register[0],
        "version_number": data_register[3],
        "current_device_status": data_coil,
        "total_product_count": data_register[6],
        "total_running_time": data_register[8],
        "total_power_on_time": data_register[10],
        "fault_code": data_register[12]
    }
    return jsonify(data_response)

if __name__ == '__main__':
    # threading.Thread(target=readDataPlc, daemon= True).start()
    # app.run(host="0.0.0.0", port=5500, debug=False)
    try:
        readDataPlc()
    except KeyboardInterrupt:
        print("exit")
