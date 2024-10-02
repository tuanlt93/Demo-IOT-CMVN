import requests
import pyodbc
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
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            return response.json()
        else:
            print('Failed to fetch data from API, status code:', response.status_code)
            return None
    except requests.exceptions.RequestException as e:
        print('Failed to fetch data from API:', e)
        return None

# Hàm lưu dữ liệu vào database
def save_data_to_db(data, db_config):
    # Thiết lập kết nối
    conn = pyodbc.connect(
        f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={db_config['server']};DATABASE={db_config['database']};UID={db_config['username']};PWD={db_config['password']}"
    )
    cursor = conn.cursor()

    # Tạo bảng nếu chưa tồn tại
    cursor.execute('''
    IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='MachineData' AND xtype='U')
    CREATE TABLE MachineData (
        MachineName NVARCHAR(50),
        MachineModel NVARCHAR(50),
        MachineCode NVARCHAR(50),
        FixedAssetCode NVARCHAR(50),
        VersionNumber NVARCHAR(50),
        FaultCode NVARCHAR(50),
        NumberIdle INT,
        TotalRunningTime INT,
        TotalPowerOnTime INT,
        QuantityProduct INT,
        RecordTime DATETIME
    )
    ''')

    cursor.execute('''
    IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='MachineSummary' AND xtype='U')
    CREATE TABLE MachineSummary (
        RecordDate DATE PRIMARY KEY,
        MachineName NVARCHAR(50),
        MachineModel NVARCHAR(50),
        MachineCode NVARCHAR(50),
        FixedAssetCode NVARCHAR(50),
        VersionNumber NVARCHAR(50),
        FaultCode NVARCHAR(50),
        NumberIdle INT,
        TotalRunningTime INT,
        TotalPowerOnTime INT,
        QuantityProduct INT
    )
    ''')

    # Chèn dữ liệu vào bảng MachineData
    cursor.execute('''
    INSERT INTO MachineData (MachineName, MachineModel, MachineCode, FixedAssetCode, VersionNumber, FaultCode, NumberIdle, TotalRunningTime, TotalPowerOnTime, QuantityProduct, RecordTime)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', ('H&E-14', 'BK-SMT30', '240221HE31020', '402000000422', '3.0', data["error"], data["number_idle"], data["running_time"], data["power_on_time"], data["quantity"], datetime.datetime.now()))

    # Lấy ngày hiện tại
    current_date = datetime.datetime.now().strftime('%Y-%m-%d')

    # Cập nhật hoặc chèn dữ liệu vào bảng tổng hợp
    cursor.execute('''
    IF EXISTS (SELECT * FROM MachineSummary WHERE RecordDate = ?)
        UPDATE MachineSummary
        SET MachineName = ?, MachineModel = ?, MachineCode = ?, FixedAssetCode = ?, VersionNumber = ?, FaultCode = ?, NumberIdle = ?, TotalRunningTime = ?, TotalPowerOnTime = ?, QuantityProduct = ?
        WHERE RecordDate = ?
    ELSE
        INSERT INTO MachineSummary (RecordDate, MachineName, MachineModel, MachineCode, FixedAssetCode, VersionNumber, FaultCode, NumberIdle, TotalRunningTime, TotalPowerOnTime, QuantityProduct)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', current_date, 'H&E-14', 'BK-SMT30', '240221HE31020', '402000000422', '3.0', data["error"], data["number_idle"], data["running_time"], data["power_on_time"], data["quantity"], current_date, current_date, 'H&E-14', 'BK-SMT30', '240221HE31020', '402000000422', '3.0', data["error"], data["number_idle"], data["running_time"], data["power_on_time"], data["quantity"])

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
        print("READ DONE")
    else:
        print('Error in data received from API')

if __name__ == "__main__":
    try:
        while True:
            main()
            time.sleep(300)
    except KeyboardInterrupt:
        print("EXIT")
