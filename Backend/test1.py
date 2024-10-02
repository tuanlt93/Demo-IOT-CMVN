from pymodbus.client.sync import ModbusSerialClient

# Thông tin kết nối serial
port = 'COM3'  # Thay đổi thành cổng serial của bạn, ví dụ COM3 trên Windows hoặc /dev/ttyUSB0 trên Linux
baudrate = 9600  # Tốc độ baud của kết nối serial
parity = 'E'  # Parity, có thể là 'N', 'E', hoặc 'O'
stopbits = 1  # Số bit dừng
bytesize = 8  # Số bit dữ liệu

# Tạo client Modbus Serial
client = ModbusSerialClient(method='rtu', port=port, baudrate=baudrate, parity=parity, stopbits=stopbits, bytesize=bytesize, timeout=1)

# Kết nối với thiết bị
connection = client.connect()

if connection:
    # Địa chỉ của bit M408 (phụ thuộc vào thiết bị của bạn, đây chỉ là ví dụ)
    # Thông thường, bit M408 sẽ nằm trong một range của các địa chỉ coils hoặc discrete inputs.
    # Ở đây, giả sử nó nằm trong các địa chỉ coils và địa chỉ offset là 407.
    address = 2456

    # Đọc giá trị của bit M408 (địa chỉ offset là 407)
    result = client.read_coils(address, 1, unit=1)  # Địa chỉ unit thường là 1, bạn có thể thay đổi nếu cần

    # Kiểm tra kết quả và in giá trị của bit M408
    if not result.isError():
        # Lấy giá trị của bit đầu tiên trong kết quả
        value = result.bits[0]
        print(f'Giá trị của bit M408 là: {value}')
    else:
        print(f'Lỗi khi đọc bit M408: {result}')
else:
    print('Không thể kết nối với thiết bị Modbus')

# Đóng kết nối
client.close()
