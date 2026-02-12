import socket
import time

#This is mainly just for testing
def new_ping(message, sock):
    sock.sendall(message.encode())
    data = sock.recv(1024)
    print(f"Received from server: {data.decode()}")
    return data


def main():
    HOST = '127.0.0.1'  # The server's hostname or IP address
    PORT = 65432  # The port used by the server

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            print(f"Connected to server {HOST}:{PORT}")

            while True:
                print("\nWhat would you like to do?")
                print("[1] ping  [2] ping many  [3] kill connection")
                user_input = input()

                if user_input == "1" or user_input == "ping":
                    data = new_ping("Buy Ticket", s)
                    if "SCAMMER" in data.decode():
                        print("Banned from server.")
                        break

                elif user_input == "2" or user_input == "ping many":
                    #Simulates the bot behavior
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

    except ConnectionResetError:
        print(f"Failed to connect to listening port {PORT}")
    except Exception as e:
        print(f"Connection ended: {e}")


if __name__ == "__main__":
    main()