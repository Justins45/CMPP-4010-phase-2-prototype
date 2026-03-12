class Connector:

    def __init__(self):
        self.IP_ADDRESS = ""
        self.timed_count = 0
        self.total_count = 0

    def set_ip(self, new_ip):
        self.IP_ADDRESS = new_ip

    def get_ip(self):
        return self.IP_ADDRESS

    def increment_count(self):
        self.timed_count += 1
        self.total_count += 1

    def decrement_timed(self):
        self.timed_count -= 1

    def reset_timed(self):
           self.timed_count = 0

    def get_timed_count(self):
        return self.timed_count

    def get_total_count(self):
        return self.total_count


