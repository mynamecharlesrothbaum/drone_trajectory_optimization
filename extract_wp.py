import re
from pymavlink import mavutil
import time

def connect(port):
    connection = mavutil.mavlink_connection(f'udpin:0.0.0.0:{port}') 

    connection.wait_heartbeat() #wait until we hear a heartbeat from the copter

    return connection 

def arm(mavlink_connection):
    """
    Arms vehicle and fly to a target altitude.
    :param mavlink_connection: The connection to the vehicle
    :param target_altitude: Target altitude in meters
    """

    print("Basic pre-arm checks")
    # Wait for vehicle to initialize and become ready
    while not mavlink_connection.wait_heartbeat(timeout=5):
        print("Waiting for vehicle heartbeat")

           
    print("Setting vehicle to GUIDED mode")
    mavlink_connection.mav.set_mode_send(mavlink_connection.target_system, mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED, 4) 

    # Wait a bit for the mode to change
    time.sleep(2)

    # Copter should arm in GUIDED mode
    mavlink_connection.mav.command_long_send(
        mavlink_connection.target_system, mavlink_connection.target_component,
        mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
        0,  # Confirmation
        1,  # 1 to arm
        0, 0, 0, 0, 0, 0  # Unused parameters for this command
    )
    
def takeoff(mavlink_connection, alt=10):
    #Assumes you have already set to guided mode and armed.

    mavlink_connection.mav.command_long_send(mavlink_connection.target_system, mavlink_connection.target_component, 
                                 mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 0, 0, 0, 0, 0, 0, 0, alt)
    
    #See how the copter responded to the takeoff command
    msg = mavlink_connection.recv_match(type = 'COMMAND_ACK', blocking = True)
    print(msg)

    while True:
        # Wait for the next LOCAL_POSITION_NED message
        msg = mavlink_connection.recv_match(type='LOCAL_POSITION_NED', blocking=True)
        
    
        # Check if altitude is within a threshold of the target altitude
        if abs(msg.z * -1 - alt) < 1.0:
            print("Reached target altitude")
            break
        
def send_waypoint_local(connection, x, y, alt):
    connection.mav.send(mavutil.mavlink.MAVLink_set_position_target_local_ned_message
                    (10, connection.target_system, connection.target_component, mavutil.mavlink.MAV_FRAME_LOCAL_NED, 
                     int(0b010111111000), x, y, alt,
                      0, 0, 0, 0, 0, 0, 0, 0))

    time.sleep(1)

# Sample input data, assuming this string contains the output you provided
data = """
Instance 125 sending neurotic waypoint: 76.19670104980469, -25.36056900024414, -61.69795227050781
Instance 125 sending neurotic waypoint: 77.66107177734375, -25.489898681640625, -63.24938201904297
Instance 125 sending neurotic waypoint: 78.87040710449219, -25.596908569335938, -64.53087615966797
Instance 125 sending neurotic waypoint: 80.01029205322266, -25.70597267150879, -65.7492904663086
Instance 125 sending neurotic waypoint: 81.21206665039062, -25.83441925048828, -67.05109405517578
Instance 125 sending neurotic waypoint: 82.5644302368164, -25.992084503173828, -68.53284454345703
Instance 125 sending neurotic waypoint: 84.1028060913086, -26.183074951171875, -70.23332214355469
Instance 125 sending neurotic waypoint: 85.84429931640625, -26.40947151184082, -72.17137908935547
Instance 125 sending neurotic waypoint: 87.85997009277344, -26.6766300201416, -74.42110443115234
Instance 125 sending neurotic waypoint: 90.15669250488281, -26.984203338623047, -76.98860168457031
Instance 125 sending neurotic waypoint: 92.5682373046875, -27.313148498535156, -79.69212341308594
Instance 125 sending neurotic waypoint: 95.05665588378906, -27.657699584960938, -82.4883804321289
Instance 125 sending neurotic waypoint: 97.64017486572266, -28.01848602294922, -85.39543914794922
Instance 125 sending neurotic waypoint: 100.40575408935547, -28.404802322387695, -88.50749969482422
Instance 125 sending neurotic waypoint: 103.39026641845703, -28.82151985168457, -91.86568450927734
Instance 125 sending neurotic waypoint: 106.58319854736328, -29.266260147094727, -95.45700073242188
Instance 125 sending neurotic waypoint: 110.43537902832031, -30.142065048217773, -99.30839538574219
Instance 125 sending neurotic waypoint: 117.18125915527344, -33.50090408325195, -103.48201751708984
Instance 125 sending neurotic waypoint: 124.12950134277344, -36.99444580078125, -107.73992156982422
Instance 125 sending neurotic waypoint: 131.26611328125, -40.59315490722656, -112.09354400634766
Instance 125 sending neurotic waypoint: 138.52760314941406, -44.26875686645508, -116.51187133789062
Instance 125 sending neurotic waypoint: 177.08819580078125, -64.1241226196289, -139.66995239257812
Instance 125 sending neurotic waypoint: 185.00576782226562, -68.26903533935547, -144.3554229736328
Instance 125 sending neurotic waypoint: 224.6129150390625, -89.24791717529297, -167.5463104248047
"""

def extract_waypoints(data):
    # Regular expression to find floats in the output
    pattern = re.compile(r"([-+]?\d*\.\d+|\d+)")
    
    # Find all matches and convert them to float, then group in triples (north, east, down)
    coords = map(float, pattern.findall(data))
    waypoints = list(zip(coords, coords, coords))  # Create a list of tuples (north, east, down)

    return waypoints

def send_waypoints_to_simulation(waypoints, drone_connection):
    for north, east, down in waypoints:
        print(f"Sending waypoint: North={north}, East={east}, Down={down}")
        send_waypoint_local(drone_connection, north, east, down)

drone_connection = connect(14550)

arm(drone_connection)
time.sleep(1)
takeoff(drone_connection)
time.sleep(8)

waypoints = extract_waypoints(data)

for waypoint in waypoints:
    north, east, down = waypoint
    send_waypoint_local(drone_connection, north, east, down)
    time.sleep(1)