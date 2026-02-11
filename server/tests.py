import unittest
from main import Counter

class TestCounter(unittest.TestCase):
    def test_increment(self):
        counter = Counter()
        counter.increment()
        self.assertEqual(counter.get_count(), 1)

    def test_decrement(self):
        counter = Counter()
        counter.decrement()
        self.assertEqual(counter.get_count(), -1)

    def test_kill(self):
        counter = Counter()
        counter.kill()
        self.assertEqual(counter.get_count(), 100000000)