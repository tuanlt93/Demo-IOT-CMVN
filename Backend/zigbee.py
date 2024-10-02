import time
import serial

# Cấu hình kết nối Modbus
MODBUS_PORT = 'COM11'
MODBUS_BAUDRATE = 9600
MODBUS_PARITY = 'N'
MODBUS_STOPBITS = 1

# Cấu hình kết nối Zigbee
ZIGBEE_PORT = 'COM11'
ZIGBEE_BAUDRATE = 9600

# Địa chỉ Zigbee
COORDINATOR_ADDR = b'\x12\x34'
ROUTER_ADDR = b'\x00\x01'

# Khởi tạo kết nối Modbus
# modbus_serial = serial.Serial(MODBUS_PORT, MODBUS_BAUDRATE, parity=MODBUS_PARITY, stopbits=MODBUS_STOPBITS)

# Khởi tạo kết nối Zigbee
zigbee_serial = serial.Serial(ZIGBEE_PORT, ZIGBEE_BAUDRATE)

def send_modbus_command(command):
    # Gửi lệnh Modbus dạng hex
    modbus_serial.write(command)
    modbus_response = modbus_serial.read(10)
    return modbus_response

def pack_zigbee_frame(data, dest_addr):
    # Đóng gói dữ liệu Modbus vào khung Zigbee
    zigbee_frame = b'\xEC\x08' + dest_addr + data
    return zigbee_frame

def send_zigbee_data(data):
    # Gửi dữ liệu qua Zigbee
    zigbee_serial.write(data)

def receive_zigbee_data(source_addr):
    # Nhận lệnh từ Zigbee
    while zigbee_serial.in_waiting > 0:
        data = zigbee_serial.read(zigbee_serial.in_waiting)
        print(data)
        if data.startswith(b'\x7E') and data[3:5] == b'\x90\x00' and data[8:10] == source_addr:
            modbus_data = data[10:-4]
            return modbus_data
    return None

def main():
    for address in range(1, 71):
    # Zigbee Coordinator gửi dữ liệu Modbus đến Zigbee Router
        zigbee_message = b'\xEC\x08' + address + b'\x01\x3A\x00\x00\x00\x0A\xC5\xCD'
        send_zigbee_data(zigbee_message)
        zigbee_command = receive_zigbee_data(ROUTER_ADDR)

        print(zigbee_command)

        time.sleep(1)

if __name__ == "__main__":
    main()