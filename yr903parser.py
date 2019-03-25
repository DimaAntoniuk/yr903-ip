#!/usr/bin/python3.5

#designed by dante

import datetime
import socket
import time
from functools import reduce
import paho.mqtt.client as mqtt

HOST = '192.168.0.178'  # The NFC reader IP address
PORT = 4001  # Port where reader listens
CHECKPOINT_ID = input(); #code to identify current checkpoint
brocker = "127.0.0.1"

header_id = 0xA0

cmd_name_reset = 0x70
cmd_name_set_uart_baudrate = 0x71
cmd_name_get_firmware_version = 0x72
cmd_name_set_reader_address = 0x73
cmd_name_set_work_antenna = 0x74
cmd_name_get_work_antenna = 0x75
cmd_name_set_output_power = 0x76
cmd_name_get_output_power = 0x77
cmd_name_set_frequency_region = 0x78
cmd_name_get_frequency_region = 0x79
cmd_name_set_beeper_mode = 0x7A
cmd_name_get_reader_temperature = 0x7B
cmd_name_set_drm_mode = 0x7C
Cmd_name_get_drm_mode = 0x7D
cmd_name_read_gpio_value = 0x60
cmd_name_write_gpio_value = 0x61
cmd_name_set_ant_connection_detector = 0x62
cmd_name_get_ant_connection_detector = 0x63
cmd_name_inventory = 0x80
cmd_name_read = 0x81
cmd_name_write = 0x82
cmd_name_lock = 0x83
cmd_name_kill = 0x84
cmd_name_set_access_epc_match = 0x85
cmd_name_get_access_epc_match = 0x86
cmd_name_real_time_inventory = 0x89
cmd_name_fast_switch_ant_inventory = 0x8A
cmd_name_iso18000_6b_inventory = 0xB0
cmd_name_iso18000_6b_read = 0xB1
cmd_name_iso18000_6b_write = 0xB2
cmd_name_iso18000_6b_lock = 0xB3
cmd_name_iso18000_6b_query_lock = 0xB4
cmd_name_get_inventory_buffer = 0x90
cmd_name_get_and_reset_inventory_buffer = 0x91
cmd_name_get_inventory_buffer_tag_count = 0x92
cmd_name_reset_inventory_buffer = 0x93
cmd_name_set_buffer_data_frame_interval = 0x94
cmd_name_get_buffer_data_frame_interval = 0x95


def checkSum(b):
    moduloSum = reduce((lambda x, y: (x + y)), b)
    return (~moduloSum + 1) % 256


def packData(address, bytedata):
    header_len = 2
    p = bytearray([header_id, len(bytedata) + header_len, address]) + bytedata
    p += bytearray([checkSum(p)])
    return p


def createRealTimeInventoryPacket(address=1, channel=1):
    return packData(address, bytearray([cmd_name_real_time_inventory, channel]))


def createBufferedInventoryPacket(address=1, channel=1):
    return packData(address, bytearray([cmd_name_inventory, channel]))


def createGetAndResetInventoryBufferPacket(address=1):
    return packData(address, bytearray([cmd_name_get_and_reset_inventory_buffer]))


def createSetAntennaPacket(antenna_id, address=1):
    return packData(address, bytearray([cmd_name_set_work_antenna, antenna_id]))


def on_connect(client, userdata, rc):
     print("connected with exit code: " + str(rc))
     client.subscribe("myTopic")

def on_massage(client, userdata, massage):
     print(str(massage.payload))


# Create a new socket to handle conversation with yr903

tags = ["e280116060000206699a8abe4879", "e20000158508017719404ca149c8",
"e2005186060a0152267009d83e8a", "e20000175608012611909f4d472d"]

client = mqtt.Client("client-01");
client.on_connect = on_connect
client.on_massage = on_massage
client.connect(brocker)
#client.username_pw_set("aizylcpj", "OmekZuyH__Sh")

client.loop_start()
for tag in tags:
    timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    screen_output = CHECKPOINT_ID + " " + tag + " " + str(timestamp)
    myFile.write(screen_output + '\n')
    client.publish("myTopic", screen_output)

client.loop_stop()
client.disconnect()
