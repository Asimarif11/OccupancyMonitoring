# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 21:21:47 2024

@author: Asim Arif
"""


import paho.mqtt.client as mqtt
import threading
import logging

# Setup basic configuration for logging
logging.basicConfig(level=logging.INFO)

# This dictionary will store the occupancy data as {(x, y): value}
occupancy_data = {}
data_lock = threading.Lock()

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logging.info("Connected successfully.")
        client.subscribe("occupancy/data")
        client.subscribe("occupancy/request")
    else:
        logging.error(f"Connection failed with code {rc}")

def on_message(client, userdata, msg):
    try:
        with data_lock:
            if msg.topic == "occupancy/data":
                x, y, value = map(int, msg.payload.decode().split(','))
                occupancy_data[(x, y)] = value
                logging.info(f"Data updated at ({x}, {y}): {value}")
            elif msg.topic == "occupancy/request":
                client.publish("occupancy/response", str(occupancy_data))
                logging.info("Sent aggregated data")
    except Exception as e:
        logging.error(f"Error handling message: {str(e)}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

try:
    client.connect("localhost", 1883, 60)  # Connect to the broker on localhost
    client.loop_forever()  # Start the loop to process callbacks
except Exception as e:
    logging.error(f"Failed to connect or start loop: {str(e)}")
