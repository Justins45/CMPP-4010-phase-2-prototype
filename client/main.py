import socket
import time
import uuid
import threading

def server_listener(sock):
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                break
            print(f"{data.decode()}", flush=True)
        except:
            break

#This is mainly just for testing
def new_ping(message, sock):
    sock.sendall(message.encode())
    data = sock.recv(1024)
    #print(f"Received from server: {data.decode()}")
    #return data
    #a change so it should actually send the UUID when the server asks for it (theoretically)
    response = data.decode()

    #check if the server is asking for the cookie
    if response == "gibcookie":
        print("The server is requesting the cookie, sending the fingerprint...")
        my_cookie = send_cookie()
        sock.sendall(my_cookie.encode())

        # wait for the server's actual response after sending the cookie
        data = sock.recv(1024)
        response = data.decode()

    print(f"Received from server: {response}")
    return data

def send_cookie():
    # Python does not have a proper cookie / fingerprint unless it's an actual server
    # current implementation uses an uuid string that will be a new generation
    # on each client start/run of the script
    # We don't need to worry about UUID overlap as there is nothing else that
    # is being used by a UUID in our scripts
    return str(uuid.uuid4())


def main():
    HOST = 'server'  # The server's hostname or IP address
    PORT = 8080  # The port used by the server

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            threading.Thread(target=server_listener, args=(s,), daemon=True).start()
            s.connect((HOST, PORT))
            print(f"Connected to server {HOST}:{PORT}")

            while True:
                print("\nWhat would you like to do?")
                print("[1] ping  [2] ping many  [3] kill connection [4] Check Performance")
                user_input = input().strip()

                if user_input == "1" or user_input == "ping":
                    data = new_ping("Buy Ticket", s)
                    if "SCAMMER" in data.decode():
                        print("Banned from server.")
                        break

                elif user_input == "2" or user_input == "ping many":
                    # Simulates the bot behavior
                    for i in range(7):
                        try:
                            data = new_ping(f"Buy Ticket #{i + 1}", s)
                            if "SCAMMER" in data.decode():
                                print("Banned from server during attack.")
                                break
                            time.sleep(0.1)  # Tiny delay so it doesn't crash the socket instantly
                        except:
                            print("Connection lost.")
                            break

                elif user_input == "3" or user_input == "kill":
                    print("Killing Connection")
                    break

                elif user_input == "4" or user_input.lower() == "check performance":
                    print("Checking performance of server response time")
                    message = "performance ping"
                    start_time = time.perf_counter()


                    print("Starting loop")
                    for i in range(1000):
                        new_ping(message, s)
                        print(i)

                    print("Finished loop")
                    endtime = time.perf_counter()

                    print(f"Performance Check for 1000 pings is {endtime - start_time:.4f} seconds.")
                    break

            # TODO: setup a checker for incoming pings with data string of "gibcookie"
            #      and return said cookie using send_cookie()

    except ConnectionResetError:
        print(f"Failed to connect to listening port {PORT}")
    except Exception as e:
        print(f"Connection ended: {e}")


if __name__ == "__main__":
    main()