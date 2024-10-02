from pymodbus.server.sync import StartTcpServer, ModbusTcpServer
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.transaction import ModbusRtuFramer, ModbusBinaryFramer
import threading

def update_registers(context):
    while True:
        try:
            address = int(input("Nhập địa chỉ thanh ghi (400-500): "))
            value = int(input("Nhập giá trị cần đặt: "))
            if 400 <= address <= 500:
                context[0].setValues(3, address, [value])
                print(f"Đã đặt giá trị {value} cho thanh ghi D{address}")
            else:
                print("Địa chỉ thanh ghi không hợp lệ, vui lòng nhập lại.")
        except ValueError:
            print("Giá trị nhập không hợp lệ, vui lòng nhập lại.")

def run_modbus_server():
    # Khởi tạo dữ liệu cho các thanh ghi từ D400 đến D500
    data_block = ModbusSequentialDataBlock(399, [1]*102)  # 102 là số lượng thanh ghi từ 400 đến 501
    
    # Cấu hình slave context với slave ID là 16
    store = ModbusSlaveContext(hr=data_block)
    context = ModbusServerContext(slaves=store, single=True)

    identity = ModbusDeviceIdentification()
    identity.VendorName = 'pymodbus'
    identity.ProductCode = 'PM'
    identity.VendorUrl = 'http://github.com/riptideio/pymodbus/'
    identity.ProductName = 'pymodbus Server'
    identity.ModelName = 'pymodbus Server'
    identity.MajorMinorRevision = '1.0'

    # Khởi chạy server Modbus TCP/IP
    server_thread = threading.Thread(target=StartTcpServer, args=(context, identity), kwargs={"address": ("localhost", 5020)})
    server_thread.daemon = True
    server_thread.start()

    # Khởi chạy hàm cập nhật thanh ghi từ bàn phím
    update_registers(context)

if __name__ == "__main__":
    run_modbus_server()
