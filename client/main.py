import socket
import time

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print(f"Connected to server {HOST}:{PORT}")
    for i in range(3):
        message = f"Ping {i+1}"
        s.sendall(message.encode())
        data = s.recv(1024)
        print(f"Received from server: {data.decode()}")
        time.sleep(1)
