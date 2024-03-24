import socket

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

# Example usage
if __name__ == "__main__":
    # Start instance 0
    start_instance('0')
    # Stop instance 0
    stop_instance('0')
