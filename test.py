import unittest
import stream

class TestStream(unittest.TestCase):
    def test_dicts_from_lists(self):
        x = stream.dicts_from_lists([
            ["abc", "def", "ghi"],
            [123, 456, 789],
            ["x", "y", "z"]
        ])
        self.assertEqual(
            x.next(),
            {"abc": 123, "def": 456, "ghi": 789}
        )
        self.assertEqual(
            x.next(),
            {"abc": "x", "def": "y", "ghi": "z"}
        )
        with self.assertRaises(StopIteration):
            x.next()

if __name__ == "__main__":
    unittest.main()
