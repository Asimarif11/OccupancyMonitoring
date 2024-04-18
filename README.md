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

    bash

git clone <repository-url>

Replace <repository-url> with the URL of this GitHub repository.

Navigate to the Project Directory:

bash

cd path/to/cloned/repository

Create a Virtual Environment (optional but recommended):

bash

python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

Install Required Packages:

bash

pip install -r requirements.txt
