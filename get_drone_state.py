from pymavlink import mavutil
import math
import tkinter as tk
import socket

#stuff

# Configuration
SIM_COMPUTER_IP = '192.168.1.124'  # IP address of the simulation computer
PORT = 15000  # The same port as used by the server

def send_command(command):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((SIM_COMPUTER_IP, PORT))
        s.sendall(command.encode('utf-8'))

def start_instance(instance_id):
    send_command(f"start {instance_id}")

def stop_instance(instance_id):
    send_command(f"stop {instance_id}")


def connect(port):
    connection = mavutil.mavlink_connection('udpin:0.0.0.0:14550') 

    connection.wait_heartbeat() #wait until we hear a heartbeat from the copter

    print("Heartbeat from system (system %u component %u)" % (connection.target_system, connection.target_component))

    return connection 

def get_current_position(connection):

    msg = connection.recv_match(type='GLOBAL_POSITION_INT', blocking=True)

    latitude = msg.lat / 1E7  # Convert from int32 to degrees
    longitude = msg.lon / 1E7  # Convert from int32 to degrees
    altitude = msg.alt / 1000.0  # Convert from millimeters to meters

    return(latitude, longitude, altitude)
    #print(f"Current Position: Latitude: {latitude}, Longitude: {longitude}, Altitude: {altitude} meters")  

def main():
    start_instance(0)

    drone_connection = connect(14550)

    # Print heartbeat information
    while True:
        msg = drone_connection.recv_match(type='HEARTBEAT', blocking=True)
        if not msg:
            print("No heartbeat")
        else:
            print("Heartbeat received from system (system %u component %u)" % (msg.get_srcSystem(), msg.get_srcComponent()))
            break  # or remove to keep listening

    while True:
        lat, lon, alt = get_current_position(drone_connection)
        

if __name__ == "__main__":
    main()