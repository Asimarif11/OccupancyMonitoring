# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 21:21:47 2024

@author: Asim Arif
"""


import paho.mqtt.client as mqtt

# This dictionary will store the occupancy data as {(x, y): value}
occupancy_data = {}

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("occupancy/data")
    client.subscribe("occupancy/request")

def on_message(client, userdata, msg):
    if msg.topic == "occupancy/data":
        x, y, value = map(int, msg.payload.decode().split(','))
        occupancy_data[(x, y)] = value
        print(f"Data updated at ({x}, {y}): {value}")
    elif msg.topic == "occupancy/request":
        # When a request for aggregated data is received, send the whole dictionary
        client.publish("occupancy/response", str(occupancy_data))
        print("Sent aggregated data")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)  # Connect to the broker on localhost
client.loop_forever()  # Start the loop to process callbacks
