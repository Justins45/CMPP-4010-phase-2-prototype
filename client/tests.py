import unittest
from unittest.mock import MagicMock
from main import new_ping

class TestPings(unittest.TestCase):
    def test_ping(self):
        mock_socket = MagicMock()

        mock_socket.recv.return_value = b"PONG"
        result = new_ping("PING", mock_socket)

        mock_socket.sendall.assert_called_once_with(b"PING")
        mock_socket.recv.assert_called_once_with(1024)
        self.assertEqual(result, b"PONG")