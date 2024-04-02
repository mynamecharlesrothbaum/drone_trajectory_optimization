from pymavlink import mavutil
import math
import tkinter as tk
import socket
import time
import helper

#stuff

# Configuration
SIM_COMPUTER_IP = '192.168.1.124'  # IP address of the simulation computer
PORT = 15000  # The same port as used by the server

def send_command(command):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((SIM_COMPUTER_IP, PORT))
        s.sendall(command.encode('utf-8'))

def connect_dynamic_port(start_port, max_attempts=10):
    for attempt in range(max_attempts):
        port = start_port + attempt
        try:
            connection = mavutil.mavlink_connection(f'udpin:0.0.0.0:{port}')
            connection.wait_heartbeat()  # Wait for the first heartbeat
            print(f"Connected on UDP port {port}")
            return connection
        except OSError as e:
            if e.errno == 48:  # Address already in use
                print(f"Port {port} is in use, trying next port.")
            else:
                raise
    raise RuntimeError("Failed to connect using dynamic ports.")

def start_instance(instance_id, out_port):
    send_command(f"start {instance_id} {out_port}")

def stop_instance(instance_id):
    send_command(f"stop {instance_id}")


def connect(port):
    connection = mavutil.mavlink_connection(f'udpin:0.0.0.0:{port}') 

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
    out_port = 14550
    pid = 0

    while True:
        out_port += 1
        pid += 1
        start_instance(pid, out_port)
        print(f"starting instance {pid} on port {out_port}")
        drone_connection = connect(out_port)

        # Print heartbeat information
        while True:
            msg = drone_connection.recv_match(type='HEARTBEAT', blocking=True)
            if not msg:
                print("No heartbeat")
            else:
                print("Heartbeat received from system (system %u component %u)" % (msg.get_srcSystem(), msg.get_srcComponent()))
                break  # or remove to keep listening

        for i in range(20):
            lat, lon, alt = get_current_position(drone_connection)
            print(f'lat: {lat}')
            print(f'lon: {lon}')
            print(f'alt: {alt}')
            
            helper.collect_positions(lat, lon, alt)
        print("Data collected, time to end this simulation")

        print("plotting trajectory...")
        helper.plot_trajectory()
        print("resetting trajectory...")
        helper.reset_trajectory()

        print("Yep i am trying to stop")
        stop_instance(0)
        

if __name__ == "__main__":
    main()