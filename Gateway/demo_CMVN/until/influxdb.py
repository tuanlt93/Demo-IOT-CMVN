from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from typing import List, Tuple
from datetime import datetime
import logging

url = "http://localhost:8086"
token = ""
org = ""
bucket = "CMVN-demo"

def writeData(machine_model: int, current_status: int, product_count: int, running_time: int, power_on_time: int):
    client = InfluxDBClient(url=url, token=token, org=org)
    point = (
            Point("data_machine")
            .tag("machine_model", machine_model)
            .field("current_status", current_status)
            .field("product_count", product_count)
            .field("running_time", running_time)
            .field("power_on_time", power_on_time) 
    )

    write_api = client.write_api(write_options=SYNCHRONOUS)
    write_api.write(bucket=bucket, org=org, record=point)
    # client.close()

def queryData(time_start: str, time_stop: str, machine_model: int) :
    client = InfluxDBClient(url=url, token=token, org=org)
    query_api = client.query_api()

    query_quantity = f'''
    from(bucket: "{bucket}")
    |> range(start: {time_start}, stop: {time_stop})
    |> filter(fn: (r) => r._measurement == "data_machine")
    |> filter(fn: (r) => r._field == "product_count")
    |> filter(fn: (r) => r.machine_model == "{machine_model}")
    '''
    query_idle = f'''
    from(bucket: "{bucket}")
    |> range(start: {time_start}, stop: {time_stop})
    |> filter(fn: (r) => r._measurement == "data_machine")
    |> filter(fn: (r) => r._field == "current_status")
    |> filter(fn: (r) => r.machine_model == "{machine_model}")
    '''
    query_running_time = f'''
    from(bucket: "{bucket}")
    |> range(start: {time_start}, stop: {time_stop})
    |> filter(fn: (r) => r._measurement == "data_machine")
    |> filter(fn: (r) => r._field == "running_time")
    |> filter(fn: (r) => r.machine_model == "{machine_model}")
    '''

    query_power_on_time = f'''
    from(bucket: "{bucket}")
    |> range(start: {time_start}, stop: {time_stop})
    |> filter(fn: (r) => r._measurement == "data_machine")
    |> filter(fn: (r) => r._field == "power_on_time")
    |> filter(fn: (r) => r.machine_model == "{machine_model}")
    '''

    tables_quantity = query_api.query(query_quantity)
    tables_idle = query_api.query(query_idle)
    tables_running_time = query_api.query(query_running_time)
    tables_power_on_time = query_api.query(query_power_on_time)

    # Lấy số sản phẩm
    quantity: int = 0
    if tables_quantity:
        first_record = tables_quantity[0].records[0]
        last_record = tables_quantity[0].records[-1]
        first_value = first_record.get_value()
        last_value = last_record.get_value()
        quantity = last_value - first_value

    # Lấy thời gian máy chạy
    running_time: int = 0
    if tables_running_time:
        first_record = tables_running_time[0].records[0]
        last_record = tables_running_time[0].records[-1]
        first_value = first_record.get_value()
        last_value = last_record.get_value()
        running_time = last_value - first_value

    # Lấy tổng thời gian bật máy
    power_on_time: int = 0
    if tables_power_on_time:
        first_record = tables_power_on_time[0].records[0]
        last_record = tables_power_on_time[0].records[-1]
        first_value = first_record.get_value()
        last_value = last_record.get_value()
        power_on_time = last_value - first_value

    # Lấy số lần dừng máy quá 15p
    number_idle = 0
    previous_time = None
    if tables_idle:
        for record in tables_idle[0].records:
            current_time = record.get_time()
            value = record.get_value()
            if value > 0:
                if previous_time is not None and (current_time - previous_time).total_seconds() > 15 * 60:
                    number_idle += 1
                previous_time = current_time

    return quantity, number_idle, running_time, power_on_time

# t1 = "2024-06-25T23:00:00Z"
# t2 = "2024-06-26T20:21:11Z"

# quantity, number_idle, running_time, power_on_time = queryData(time_start= t1, time_stop= t2, machine_model= 126823)
# print(quantity, number_idle, running_time, power_on_time)
