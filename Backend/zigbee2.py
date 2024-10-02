import time
import serial
import struct

# Cấu hình kết nối Zigbee
ZIGBEE_PORT = 'COM3'
ZIGBEE_BAUDRATE = 9600

# Địa chỉ Zigbee
ROUTER_ADDR = b'\x00\x01'

zigbee_serial = serial.Serial(ZIGBEE_PORT, ZIGBEE_BAUDRATE)

def send_zigbee_data(data):
    """Gửi dữ liệu qua Zigbee."""
    zigbee_serial.write(data)
    print(f"Sent Zigbee message: {data}")

def receive_zigbee_data(source_addr):
    """Nhận lệnh từ Zigbee."""
    while zigbee_serial.in_waiting > 0:
        data = zigbee_serial.read(zigbee_serial.in_waiting)
        return data
 

def decode_modbus_zigbee(byte_sequence):
    data = byte_sequence[3:23]  
    registers = struct.unpack('>' + 'H' * 10, data)
    return list(registers)

def main():
    for address in range(1, 5):
        # Convert address to hexadecimal byte
        address_byte = address.to_bytes(1, 'big')
        
        # Zigbee Coordinator sends Modbus data to Zigbee Router
        zigbee_message = b'\xEC\x08\x00' + address_byte + b'\x01\x03\x10\x32\x00\x0A\x60\xC2'
        send_zigbee_data(zigbee_message)
        
        # Wait a short time to ensure data is available
        time.sleep(1)
        
        # Receive and decode data from Zigbee Router
        zigbee_fb = receive_zigbee_data(ROUTER_ADDR)
        print(zigbee_fb)

        if zigbee_fb:
            data_decode = decode_modbus_zigbee(zigbee_fb)
            print(data_decode)


        time.sleep(1)

if __name__ == "__main__":
    main()



