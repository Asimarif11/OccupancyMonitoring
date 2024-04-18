# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 21:54:13 2024

@author: Asim Arif
"""

import paho.mqtt.client as mqtt
import time

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("occupancy/response")

def on_message(client, userdata, msg):
    if msg.topic == "occupancy/response":
        print("Client 2 Received aggregated data: ", msg.payload.decode())
        client.disconnect()

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)
client.loop_start()

# Sending overlapping data with different values
data_points = [
    (1, 2, 1),  # Overlapping coordinate with different value
    (2, 2, 1),  # Overlapping coordinate with different value
    (3, 3, 1),  # New coordinate
    (4, 4, 1)   # New coordinate
]
for x, y, value in data_points:
    client.publish("occupancy/data", f"{x},{y},{value}")
    time.sleep(1)

# Requesting aggregated data
client.publish("occupancy/request", "get data")

time.sleep(5)  # Wait to receive data

client.loop_stop()
client.disconnect()
