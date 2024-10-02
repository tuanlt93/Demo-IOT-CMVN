from sqlalchemy import create_engine, Column, Integer, String, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import requests
from datetime import datetime
import schedule
import time

# Cấu hình kết nối đến MySQL
cfg = {
    'user': 'rostek',
    'pass': 'rostek2019',
    'host': 'localhost',
    'port': 3306,
    'scheme': 'cmvn_demo'
}

SQL_URI = f"mysql+pymysql://{cfg['user']}:{cfg['pass']}@{cfg['host']}:{cfg['port']}/{cfg['scheme']}"

# Khởi tạo engine và session
engine = create_engine(SQL_URI)
Session = sessionmaker(bind=engine)
session = Session()

# Khởi tạo cơ sở dữ liệu
Base = declarative_base()

class MachineData(Base):
    __tablename__ = 'machine_data'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    DateTime = Column(DateTime, default=func.now())
    MachineName = Column(String(255))
    MachineModel = Column(String(255))
    MachineCode = Column(String(255))
    FixedAssetCode = Column(String(255))
    VersionNumber = Column(String(255))
    FaultCode = Column(String(255))
    NumberIdle = Column(Integer)
    TotalRunningTime = Column(Integer)
    TotalPowerOnTime = Column(Integer)
    QuantityProsuct = Column(Integer)

# Tạo bảng trong cơ sở dữ liệu nếu chưa tồn tại
Base.metadata.create_all(engine)

# Hàm để gọi API và ghi dữ liệu vào MySQL
def get_and_store_data():
    try:
        # Gọi API để lấy dữ liệu
        response = requests.get("http://192.168.31.20:5001/machine/data")
        response.raise_for_status()  # Kiểm tra xem có lỗi trong quá trình gọi API không
        data = response.json()

        # Tạo đối tượng MachineData
        machine_data = MachineData(
            MachineName = "H&E-14",
            MachineModel = "BK-SMT30",
            MachineCode = "69481924g",
            FixedAssetCode = "3294fiasojd",
            VersionNumber = "3.0",
            FaultCode = "0",
            NumberIdle=data["number_idle"],
            TotalRunningTime=data["running_time"],
            TotalPowerOnTime=data["power_on_time"],
            QuantityProsuct=data["quantity"]     
        )

        # Ghi dữ liệu vào MySQL
        session.add(machine_data)
        session.commit()
        
        print("Data successfully inserted into MySQL")

    except requests.exceptions.RequestException as e:
        print(f"Error calling API: {e}")
    except Exception as e:
        session.rollback()
        print(f"Error interacting with MySQL: {e}")
    finally:
        session.close()



# # Lên lịch để chạy hàm get_and_store_data mỗi ngày vào lúc 23h00
# schedule.every().day.at("23:00").do(get_and_store_data)
# print("Scheduler started. Waiting for the scheduled time...")


# while True:
#     schedule.run_pending()
#     time.sleep(1)


get_and_store_data()
