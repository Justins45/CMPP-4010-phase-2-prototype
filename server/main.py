import socket
import threading
from time import sleep

# Configuration
HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

# Set descriptive variables so we don't have to remember what the god numbers mean
timed_max_pings = 3  # per second max
total_max_pings = 6  # total transactions

# Data Structures
# This dictionary tracks IPs: { '127.0.0.1': {'timed_count': 0, 'total_count': 0, 'banned': False} }
client_data = {}
data_lock = threading.Lock()


def decrease_counters():
    """
    Background thread that acts as the timer.
    """
    while True:
        sleep(1)
        with data_lock:
            #Loop through all known IP addresses and lower their timed count
            for ip in client_data:
                if client_data[ip]['timed_count'] > 0:
                    client_data[ip]['timed_count'] -= 1


def handle_client(conn, addr):
    ip_address = addr[0]
    print(f'Connected by {addr}')

    #Initialize this IP in our database if new
    with data_lock:
        if ip_address not in client_data:
            client_data[ip_address] = {'timed_count': 0, 'total_count': 0, 'banned': False}

    #Check if they are already banned before talking
    if client_data[ip_address]['banned']:
        print("SCAMMER GET SCAMMED (Connection Refused)")
        conn.close()
        return

    with conn:
        while True:
            try:
                data = conn.recv(1024)
                if not data:
                    break

                print(f"Received from client: {data.decode()}")

                should_ban = False

                with data_lock:
                    #Increment counts
                    client_data[ip_address]['timed_count'] += 1
                    client_data[ip_address]['total_count'] += 1

                    #Check Thresholds
                    current_timed = client_data[ip_address]['timed_count']
                    current_total = client_data[ip_address]['total_count']

                    if current_total >= total_max_pings:
                        print("SCAMMER GET SCAMMED (Total Limit)")
                        client_data[ip_address]['banned'] = True
                        should_ban = True

                    elif current_timed >= timed_max_pings:
                        print("SCAMMER GET SCAMMED (Speed Limit)")
                        client_data[ip_address]['banned'] = True
                        should_ban = True

                if should_ban:
                    #Kill the connection from the server
                    error_msg = "SCAMMER GET SCAMMED"
                    conn.sendall(error_msg.encode())
                    break
                else:
                    response = b"Pong"
                    conn.sendall(response)

            except ConnectionResetError:
                break

    # print(f"Connection closed for {ip_address}")


def main():
    #Start the imer
    timer_thread = threading.Thread(target=decrease_counters, daemon=True) #Daemon=True makes it so when the main thread ends
    #This specific thread dies immediately along with it.
    timer_thread.start()

    print(f"Server listening on {HOST}:{PORT}")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        #This line helps avoid "Address already in use" errors if you restart quickly
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        #s.fuckoff


        while True:
            conn, addr = s.accept()
            handle_client(conn, addr)


if __name__ == '__main__':
    main()