# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 21:23:40 2024

@author: Asim Arif
"""

import paho.mqtt.client as mqtt
import time

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    # Subscribe to the response topic upon successful connection
    client.subscribe("occupancy/response")

def on_message(client, userdata, msg):
    if msg.topic == "occupancy/response":
        # Print the received message
        print(f"Received aggregated data: {msg.payload.decode()}")
        # Consider adding a client disconnect here after receiving the data
        client.disconnect()

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)  # Connect to the broker

# Start a non-blocking loop to handle incoming messages and reconnections
client.loop_start()

# Sending data
data_points = [
    (1, 2, 0), (1, 3, 1), (2, 2, 0), (3, 3, 0)
]
for x, y, value in data_points:
    client.publish("occupancy/data", f"{x},{y},{value}")
    time.sleep(1)

# Requesting aggregated data
client.publish("occupancy/request", "get data")

# Allow some time for the server to respond and for message handling
time.sleep(5)  # Adjusted to wait longer

# Stop the loop and disconnect after enough time has passed
client.loop_stop()
client.disconnect()
