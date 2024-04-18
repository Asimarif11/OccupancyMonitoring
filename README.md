# Occupancy Monitoring
Overview

This project is a client-server application using MQTT to manage and monitor occupancy data. It demonstrates the handling of real-time data from multiple clients, with functionalities including data sending, updating, and requesting aggregated occupancy data. The server maintains a record of the latest occupancy status for each coordinate, which can be requested by clients at any time.
System Architecture

The system consists of three main components:

MQTT Broker: Manages messages between clients and the server.
Server: Subscribes to occupancy data and requests from clients, stores the latest data, and sends aggregated data upon request.
Clients: Send occupancy data to the server and can request aggregated occupancy data. Two sample clients are provided to demonstrate overlapping coordinates with differing occupancy values.

Setup Instructions
Prerequisites

Python: Ensure Python 3.x is installed on your system.
MQTT Broker: Mosquitto or any other MQTT broker must be installed and running on your system.

Installation

Clone the Repository:


    git clone <repository-url>

Replace <repository-url> with the URL of this GitHub repository.

Navigate to the Project Directory:


    cd path/to/cloned/repository

Create a Virtual Environment (optional but recommended):


    python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

Install Required Packages (Please note that Spyder IDE was used and therefore includes packages related to ipython console):


    pip install -r requirements.txt
    
If not using Spyder IDE, just install paho MQTT library ( Note that teh version is important, the latest version has errors related to the Callback argument when initializing
mqtt.client class)

    pip install paho-mqtt==1.6.1

Running the Application

Start the MQTT Broker:
Ensure that your MQTT broker is running on the default port (usually 1883). If Mosquitto is installed and on windows, search services and find Mosquitto Broker and start it.

Run the Server:

    python src/client.py
    
Run the Client:

    python src/client.py

Run Client2:

    python src/client2.py

Detailed Functionality

Server:
        Listens for data on the occupancy/data topic.
        Stores or updates occupancy data based on the latest messages received.
        On receiving a request on occupancy/request, sends the aggregated occupancy data to occupancy/response.

Clients:
        Send data to occupancy/data with coordinates and occupancy status.
        Request aggregated data from occupancy/request.
        The example clients are set up to demonstrate overlapping coordinates with different occupancy values. Depending on the sequence of execution, the final aggregated data seen by running client2.py will reflect the latest updates by either client.
