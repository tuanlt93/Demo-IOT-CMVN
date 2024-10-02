import pyads
import time

class MockPLC:
    def __init__(self, ams_net_id, port, ip):
        self.ams_net_id = ams_net_id
        self.port = port
        self.ip = ip
        self.variables = {
            'Input.X4_Alarm': False,
            'Input.X10_SS1': True,
            'Input.X11_SS2': False,
            'Output.Y6_Spare': True
        }

    def open(self):
        print("Mô phỏng: Kết nối mở")

    def close(self):
        print("Mô phỏng: Kết nối đóng")

    def read_by_name(self, var_name, var_type):
        if var_name in self.variables:
            return self.variables[var_name]
        else:
            raise ValueError(f"Biến {var_name} không tồn tại trong mô phỏng")


# Địa chỉ IP của thiết bị Beckhoff và AMS Net ID của máy tính
PLC_IP = '192.168.125.10'
AMS_NET_ID = '5.123.146.180.1.1'

# Tạo kết nối với thiết bị Beckhoff (giả lập)
plc = MockPLC(AMS_NET_ID, pyads.PORT_TC3PLC1, PLC_IP)

# Mở kết nối
plc.open()

try:
    time1 = time.time()
    variables = [
        ('db_status.Mode', pyads.PLCTYPE_BOOL),
        ('gvl_data.SL_OK', pyads.PLCTYPE_BOOL),
        ('gvl_data.SL_NG', pyads.PLCTYPE_BOOL),
        ('gvl_data.Time_Run', pyads.PLCTYPE_BOOL),
        ('gvl_data.Time_Stop', pyads.PLCTYPE_BOOL),
        ('gvl_data.Model', pyads.PLCTYPE_BOOL),
        ('gvl_data.Model', pyads.PLCTYPE_BOOL),
    ]

    # Đọc dữ liệu từ các biến trong PLC
    for item in variables:
        if item['type'] == 'BOOL':
            value = self.plc.read_by_name(item['name'], pyads.PLCTYPE_BOOL)
        elif item['type'] == 'INT':
            value = self.plc.read_by_name(item['name'], pyads.PLCTYPE_INT)
        elif item['type'] == 'LINT':
            value = self.plc.read_by_name(item['name'], pyads.PLCTYPE_LINT)
        elif item['type'] == 'STRING':
            value = self.plc.read_by_name(item['name'], pyads.PLCTYPE_STRING)
        elif item['type'] == 'DWORD':
            value = self.plc.read_by_name(item['name'], pyads.PLCTYPE_DWORD)
        elif item['type'] == 'WORD':
            value = self.plc.read_by_name(item['name'], pyads.PLCTYPE_WORD)
        elif item['type'] == 'REAL':
            value = self.plc.read_by_name(item['name'], pyads.PLCTYPE_REAL)
        elif item['type'] == 'LREAL':
            value = self.plc.read_by_name(item['name'], pyads.PLCTYPE_LREAL)
        else: value = None
        
    values[item['name']] = value

    time2 = time.time()
    print(time2 - time1)
except Exception as e:
    print(f'Không thể đọc dữ liệu: {e}')

# Đóng kết nối
plc.close()
