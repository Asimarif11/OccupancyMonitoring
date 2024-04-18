# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 21:23:40 2024

@author: Asim Arif
"""

import paho.mqtt.client as mqtt
import time
import logging

# Setup basic configuration for logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logging.info("Client 2 connected successfully.")
        client.subscribe("occupancy/response")
    else:
        logging.error(f"Client 2 failed to connect, return code {rc}")

def on_disconnect(client, userdata, rc):
    if rc != 0:
        logging.warning("Client 2 unexpectedly disconnected.")
        try:
            client.reconnect()
        except Exception as e:
            logging.error(f"Client 2 reconnection failed: {str(e)}")

def on_message(client, userdata, msg):
    if msg.topic == "occupancy/response":
        logging.info(f"Client 2 received aggregated data: {msg.payload.decode()}")
        client.disconnect()

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect

try:
    client.connect("localhost", 1883, 60)  # Connect to the broker
    client.loop_start()  # Start a non-blocking loop to handle incoming messages and reconnections

    # Sending overlapping data with different values
    data_points = [
        (1, 2, 1),  # Overlapping coordinate with different value
        (2, 2, 1),  # Overlapping coordinate with different value
        (3, 3, 1),  # New coordinate
        (4, 4, 1)   # New coordinate
    ]
    for x, y, value in data_points:
        payload = f"{x},{y},{value}"
        client.publish("occupancy/data", payload)
        logging.info(f"Client 2 sent data: {payload}")
        time.sleep(1)

    # Requesting aggregated data
    client.publish("occupancy/request", "get data")
    time.sleep(5)  # Wait to receive data

    client.loop_stop()  # Stop the loop
    client.disconnect()  # Disconnect cleanly
except Exception as e:
    logging.error(f"Client 2 operation failed: {str(e)}")
