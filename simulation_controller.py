import socket
import subprocess
import os

host = '0.0.0.0'

port = 15000

processes = {}


def start_instance_sitl(instance_id):
    cmd = f"sim_vehicle.py -v ArduCopter -f gazebo-iris -L RADY --console --map --out 192.168.1.40:14550"

    process = subprocess.Popen(cmd, shell=True)

    processes[instance_id] = process

    print(f"Started instance {instance_id} with PID {process.pid}")


def stop_instance_sitl(instance_id):
    if instance_id in processes:
        processes[instance_id].terminate()

def handle_command(command):
    parts = command.split()

    if parts[0] == 'start':
        start_instance_sitl(parts[1])

    elif parts[0] == 'stop':
        stop_instance_sitl(parts[1])
    else:
        print("i don't know that command")

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"listening on {host} : {port}")

        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                command = data.decode('utf-8')
                handle_command(command)

if __name__ == "__main__":
    main()
