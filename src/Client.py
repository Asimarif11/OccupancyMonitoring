# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 21:23:40 2024

@author: Asim Arif
"""

import paho.mqtt.client as mqtt
import time
import logging

# Setup basic configuration for logging
logging.basicConfig(level=logging.INFO)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logging.info("Connected successfully.")
        client.subscribe("occupancy/response")
    else:
        logging.error(f"Failed to connect, return code {rc}")

def on_disconnect(client, userdata, rc):
    if rc != 0:
        logging.warning("Unexpected disconnection.")
        try:
            client.reconnect()
        except Exception as e:
            logging.error(f"Reconnection failed: {str(e)}")

def on_message(client, userdata, msg):
    if msg.topic == "occupancy/response":
        logging.info(f"Received aggregated data: {msg.payload.decode()}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect

try:
    client.connect("localhost", 1883, 60)  # Connect to the broker
    client.loop_start()  # Start a non-blocking loop to handle incoming messages and reconnections

    # Sending data
    data_points = [
        (1, 2, 0), (1, 3, 1), (2, 2, 0), (2, 3, 0)
    ]
    for x, y, value in data_points:
        payload = f"{x},{y},{value}"
        client.publish("occupancy/data", payload)
        logging.info(f"Sent data: {payload}")
        time.sleep(1)

    # Requesting aggregated data
    client.publish("occupancy/request", "get data")
    time.sleep(5)  # Wait to receive data

    client.loop_stop()  # Stop the loop
    client.disconnect()  # Disconnect cleanly
except Exception as e:
    logging.error(f"Operation failed: {str(e)}")
