import unittest
from main import Connector

class TestConnector(unittest.TestCase):


    def set_set_ip(self):
        connector = Connector()
        connector.set_ip("wasda")
        self.assertEqual(connector.get_ip(), "wasda")

    def test_increment(self):
        connector = Connector()
        connector.increment_count()
        self.assertEqual(connector.timed_count, 1)
        self.assertEqual(connector.total_count, 1)


    def test_decrement(self):
        connector = Connector()
        connector.decrement_timed()
        self.assertEqual(connector.timed_count, -1)

    def test_reset_timed(self):
        connector = Connector()
        connector.increment_count()
        connector.decrement_timed()
        self.assertEqual(connector.timed_count, 0)
