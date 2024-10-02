from digi.xbee.devices import XBeeDevice
from digi.xbee.exception import InvalidOperatingModeException, XBeeException

# Cổng và tốc độ baud của thiết bị Zigbee (coordinator)
port = "COM4"  # Thay đổi cổng phù hợp với hệ thống của bạn
baud_rate = 9600

# Khởi tạo thiết bị Zigbee (coordinator)
device = XBeeDevice(port, baud_rate)

try:
    print("Opening device...")
    device.open()
    print("Device opened successfully!")

except InvalidOperatingModeException as e:
    print("Invalid operating mode: ", e)
except XBeeException as e:
    print("Error opening device: ", e)
finally:
    # Đóng thiết bị Zigbee
    if device is not None and device.is_open():
        device.close()
