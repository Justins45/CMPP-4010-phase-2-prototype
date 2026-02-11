import socket

from threading import Thread, Event
from time import sleep


class Counter:
    def __init__(self):
        self.count = 0

    def increment(self):
        self.count += 1

    def decrement(self):
        self.count -= 1

    def get_count(self):
        return self.count

    def kill(self):
        self.count = 100000000

def main():
    HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
    PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

    # Set descriptive variables so we don't have to remember what the god numbers mean
    timed_max_pings = 3  # per second max
    total_max_pings = 6  # total transactions

    # Set up counters
    ping_count_timed = Counter()
    ping_count_total = Counter()

    def count_check():
        # print("COUNT CHECKING")
        print(ping_count_timed.get_count())
        if ping_count_timed.get_count() >= timed_max_pings:
            ping_count_timed.kill()
        elif ping_count_timed.get_count() > 0:
            ping_count_timed.decrement()

    def thread_function(evt):
        while not evt.is_set():
            # print("THREAD FUNCTION")
            count_check()
            sleep(1)

    # Start Timer
    thread = Thread(target=thread_function, args=(Event(),))
    thread.start()
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen()
            print(f"Server listening on {HOST}:{PORT}")
            conn, addr = s.accept()
            with conn:
                print(f'Connected by {addr}')
                while True:
                    data = conn.recv(1024)
                    print(f"Received from client: {data.decode()}")
                    response = b"Pong"
                    conn.sendall(response)

                    ping_count_timed.increment()
                    ping_count_total.increment()
                    if ping_count_total.get_count() >= total_max_pings:
                        print("SCAMMER GET SCAMMED")
                        break
                    elif ping_count_timed.get_count() >= timed_max_pings:
                        print("SCAMMER GET SCAMMED")
                        break
                    else:
                        continue
    except ConnectionResetError:
        print(f"Failed to connect to listening port {PORT}")

if __name__ == '__main__':
    main()