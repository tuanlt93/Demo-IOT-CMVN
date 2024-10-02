import requests
import mysql.connector
import datetime
import yaml
import time

# Hàm để đọc cấu hình từ file YAML
def load_config(config_file='config.yaml'):
    with open(config_file, 'r') as file:
        config = yaml.safe_load(file)
    return config

# Hàm lấy dữ liệu từ API
def fetch_data(api_url):
    data = {
        "machine_model": "0",
        "number_idle": 1,
        "power_on_time": 0,
        "quantity": 0,
        "running_time": 0,
        "error":200
    }
    # try:
    #     response = requests.get(api_url)
    #     if response.status_code == 200:
    #         return response.json()
    #     else:
    #         print('Failed to fetch data from API, status code:', response.status_code)
    #         return None
    # except requests.exceptions.RequestException as e:
    #     print('Failed to fetch data from API:', e)
    #     return None
    return data

# Hàm lưu dữ liệu vào database
def save_data_to_db(data, db_config):
    # Thiết lập kết nối
    conn = mysql.connector.connect(
        host=db_config['server'],
        user=db_config['username'],
        password=db_config['password'],
        database=db_config['database']
    )
    cursor = conn.cursor()

    # Lấy ngày hiện tại
    current_date = datetime.datetime.now().strftime('%Y%m%d')
    current_date_str = datetime.datetime.now().strftime('%Y-%m-%d')

    # Tạo bảng nếu chưa tồn tại
    daily_table_name = f'MachineData_{current_date}'
    summary_table_name = 'MachineSummary'

    cursor.execute(f'''
    CREATE TABLE IF NOT EXISTS {daily_table_name} (
        MachineName VARCHAR(50),
        MachineModel VARCHAR(50),
        MachineCode VARCHAR(50),
        FixedAssetCode VARCHAR(50),
        VersionNumber VARCHAR(50),
        FaultCode VARCHAR(50),
        NumberIdle INT,
        TotalRunningTime INT,
        TotalPowerOnTime INT,
        QuantityProduct INT,
        RecordTime DATETIME
    )
    ''')

    cursor.execute(f'''
    CREATE TABLE IF NOT EXISTS {summary_table_name} (
        RecordDate DATE PRIMARY KEY,
        MachineName VARCHAR(50),
        MachineModel VARCHAR(50),
        MachineCode VARCHAR(50),
        FixedAssetCode VARCHAR(50),
        VersionNumber VARCHAR(50),
        FaultCode VARCHAR(50),
        NumberIdle INT,
        TotalRunningTime INT,
        TotalPowerOnTime INT,
        QuantityProduct INT
    )
    ''')

    # Chèn dữ liệu vào bảng theo ngày
    cursor.execute(f'''
    INSERT INTO {daily_table_name} (MachineName, MachineModel, MachineCode, FixedAssetCode, VersionNumber, FaultCode, NumberIdle, TotalRunningTime, TotalPowerOnTime, QuantityProduct, RecordTime)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ''', ('H&E-14', 'BK-SMT30', '240411HE31004', '402000011271', '3.0', data["error"], data["number_idle"], data["running_time"], data["power_on_time"], data["quantity"], datetime.datetime.now()))

    # Cập nhật hoặc chèn dữ liệu vào bảng tổng hợp
    cursor.execute(f'''
    INSERT INTO {summary_table_name} (RecordDate, MachineName, MachineModel, MachineCode, FixedAssetCode, VersionNumber, FaultCode, NumberIdle, TotalRunningTime, TotalPowerOnTime, QuantityProduct)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
        MachineName = VALUES(MachineName),
        MachineModel = VALUES(MachineModel),
        MachineCode = VALUES(MachineCode),
        FixedAssetCode = VALUES(FixedAssetCode),
        VersionNumber = VALUES(VersionNumber),
        FaultCode = VALUES(FaultCode),
        NumberIdle = VALUES(NumberIdle),
        TotalRunningTime = VALUES(TotalRunningTime),
        TotalPowerOnTime = VALUES(TotalPowerOnTime),
        QuantityProduct = VALUES(QuantityProduct)
    ''', (current_date_str, 'H&E-14', 'BK-SMT30', '240411HE31004', '402000011271', '3.0', data["error"], data["number_idle"], data["running_time"], data["power_on_time"], data["quantity"]))

    # Lưu thay đổi và đóng kết nối
    conn.commit()
    cursor.close()
    conn.close()

# Hàm chính
def main():
    config = load_config()
    api_url = config['api']['url']
    db_config = config['database']
    
    data = fetch_data(api_url)
    if data:
        save_data_to_db(data, db_config)
    else:
        print('Error in data received from API')

if __name__ == "__main__":
    try:
        while True:
            main()
            print("READ DONE")
            time.sleep(30)
    except KeyboardInterrupt:
        print("EXIT")
