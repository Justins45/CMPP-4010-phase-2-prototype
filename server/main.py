import socket
import threading
from time import sleep
import connector
import datetime

# Configuration
HOST = '0.0.0.0'  # Standard loopback interface address (localhost)
PORT = 8080  # Port to listen on (non-privileged ports are > 1023)

# Set descriptive variables so we don't have to remember what the god numbers mean
timed_max_pings = 3  # per second max
total_max_pings = 6  # total transactions

# Data Structures
client_data = connector.Connector()
data_lock = threading.Lock()


def decrease_counters():
    """
    Background thread that acts as the timer.
    """
    while True:
        sleep(1)
        with data_lock:
            # Lower times count
            if client_data.get_timed_count() > 0:
                client_data.decrement_timed()


def handle_client(conn, addr):
    client_data.set_ip(addr[0])
    print(f'Connected by {addr}')

    with conn:
        while True:
            try:
                data = conn.recv(1024)
                if not data:
                    break

                print(f"Received from client: {data.decode()}")

                should_ban = False

                # TODO: check each request for a cookie thats sent and add to
                #       the client data

                with data_lock:
                    #Increment counts
                    client_data.increment_count()

                    if client_data.get_total_count() >= total_max_pings:
                        print("SCAMMER GET SCAMMED (Total Limit)")
                        should_ban = True

                    elif client_data.get_timed_count() >= timed_max_pings:
                        print("SCAMMER GET SCAMMED (Speed Limit)")
                        should_ban = True

                    # If the request is two thirds of the timed max ping OR two thirds the total pings allowed
                    # Request the users cooke data to check for scammer activities
                    if client_data.get_timed_count() == (2/3) * timed_max_pings or client_data.get_total_count() == (
                            2/3) * total_max_pings:
                        request_cookie(conn)

                if should_ban:
                    kill_fn(conn, client_data)
                    break
                else:
                    response = b"Pong"
                    conn.sendall(response)

            except ConnectionResetError:
                break


def add_scammer_to_db(ip_address):
    file_path = 'scammers_ips.txt'
    date = datetime.datetime.now()
    new_line_content = f"{ip_address}, {date}"

    # Add scammer IP to database
    with open(file_path, 'a') as file:
        file.write('\n')
        file.write(new_line_content)
        print("Scammer data added to db :)")

def kill_fn(conn, data):
    # Kill the connection from the server
    error_msg = "SCAMMER GET SCAMMED"
    conn.sendall(error_msg.encode())
    add_scammer_to_db(data.IP_ADDRESS)
    conn.close()
    # conn.fuckoff

def request_cookie(conn):
    conn.sendall("gibcookie".encode())

def main():
    # Start the imer
    timer_thread = threading.Thread(target=decrease_counters, daemon=True) #Daemon=True makes it so when the main thread ends
    # This specific thread dies immediately along with it.
    timer_thread.start()

    print(f"Server listening on {HOST}:{PORT}")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # This line helps avoid "Address already in use" errors if you restart quickly
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()

        while True:
            conn, addr = s.accept()
            # Makes a new thread for every person who connects
            client_thread = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
            client_thread.start()
            
            #conn, addr = s.accept()
            #handle_client(conn, addr)


if __name__ == "__main__":
    main()