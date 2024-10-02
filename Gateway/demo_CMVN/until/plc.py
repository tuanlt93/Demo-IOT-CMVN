from pymodbus.register_write_message import WriteSingleRegisterResponse as SUCCESS
from pymodbus.client.sync import ModbusSerialClient
from time import sleep
import threading
import redis

lock = threading.Lock()

class PLCStation:
    def __init__(self, serial_port, baudrate =9600, timeout = 0.5):
        self.serial_port = serial_port
        self.baudrate = baudrate
        self.timeout = timeout

        self.client = ModbusSerialClient(
            method='rtu',
            port=self.serial_port,
            baudrate=self.baudrate,
            timeout=self.timeout,
            bytesize=8,
            stopbits=1,
            parity="E"
        )
        # self.client = ModbusSerialClient(
        #     method='ascii',
        #     port=self.serial_port,
        #     baudrate=self.baudrate,
        #     timeout=self.timeout,
        #     bytesize=7,
        #     stopbits=1,
        #     parity="E"
        # )
        self.client.connect()

    def read_registers(self) -> list[int]:
        cnt = 0
        while True:
            with lock:
                data = self.client.read_holding_registers(address=40768, count=13, unit=1)
                if hasattr(data, 'registers'):
                    processed_data = data.registers
                    return processed_data
                else:
                    cnt += 1
                    sleep(0.2)
                if cnt == 1:
                    # print(f"Give up reading to PLC: 1")
                    return [0]*13  

    def read_coil(self) -> int:
        cnt = 0
        while True:
            with lock:
                result = self.client.read_coils(address=2456, count=1, unit=1) 
                if not result.isError():
                    coil_value = result.bits[0]
                    return int(coil_value)
                else:
                    cnt += 1
                    sleep(0.2)
                if cnt == 1:
                    # print(f"Give up reading to PLC: 1")
                    return 0 





# community_PLC = PLCStation(serial_port="/dev/serial/by-path/platform-fe9c0000.xhci-usb-0:1.4:1.0-port0", baudrate=9600, timeout=1)
# data_register = community_PLC.read_registers()
# data_coil = community_PLC.read_coil()

# print(data_register)
# print(data_coil)