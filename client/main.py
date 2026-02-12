import socket

def new_ping(message, sock):
    sock.sendall(message.encode())
    data = sock.recv(1024)
    print(f"Received from server: {data.decode()}")
    return data

def main():
    HOST = '127.0.0.1'  # The server's hostname or IP address
    PORT = 65432        # The port used by the server

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            print(f"Connected to server {HOST}:{PORT}")
            while True:
                print("What would you like to do?")
                user_input = input()
                if user_input == "ping":
                    new_ping("Buy Ticket", s)
                    continue
                elif user_input == "ping many":
                    for i in range(7):
                        new_ping(f"Buy Ticket #{i+1}", s)
                    continue
                elif user_input == "kill":
                    print("Killing Connection")
                    break

    except ConnectionResetError:
        print(f"Failed to connect to listening port {PORT}")

if __name__ == "__main__":
    main()