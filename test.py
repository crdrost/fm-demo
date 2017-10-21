import unittest
import stream
import datetime

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

    def test_gpscans_from_dicts(self):
        x = stream.gpscans_from_dicts([{
            'message_id': '', 'dlc': '', 'payload': '', 'puc_id': '8765',
            'ts': '2016-10-28 05:00:00', 'gps_id': '681665533',
            'latitude': '35.05875000000000', 'longitude': '-80.38093000000000',
            'groundspeed': '0.01841250000000', 'truecourse': '0.00000000000000'
        }, {
            'message_id': '0CFF1003', 'dlc': '8', 'payload': 'FFFFFFFFFFFFFFFF',
            'puc_id': '8765', 'ts': '2016-10-28 05:00:00', 'gps_id': '',
            'latitude': '', 'longitude': '', 'groundspeed': '', 'truecourse': ''
        }, {
            'message_id': '1CFFFF17', 'dlc': '8', 'payload': '9AFF64FFFFFFFFFF',
            'puc_id': '8765', 'ts': '2016-10-28 05:00:00', 'gps_id': '',
            'latitude': '', 'longitude': '', 'groundspeed': '', 'truecourse': ''
        }, {
            'message_id': '0CFFFE17', 'dlc': '8', 'payload': '3317FFFFFFFFFFFF',
            'puc_id': '8765', 'ts': '2016-10-28 05:00:00', 'gps_id': '',
            'latitude': '', 'longitude': '', 'groundspeed': '', 'truecourse': ''
        }])
        d = datetime.datetime(2016, 10, 28, 5, 0, 0)
        self.assertEqual(
            x.next(),
            ('gps', d, 8765, (681665533, 35.05875, -80.38093, 0.0184125, 0.0))
        )
        self.assertEqual(
            x.next(),
            ('can', d, 8765, ('0CFF1003', 8, 'FFFFFFFFFFFFFFFF'))
        )
        self.assertEqual(
            x.next(),
            ('can', d, 8765, ('1CFFFF17', 8, '9AFF64FFFFFFFFFF'))
        )
        self.assertEqual(
            x.next(),
            ('can', d, 8765, ('0CFFFE17', 8, '3317FFFFFFFFFFFF'))
        )
        with self.assertRaises(StopIteration):
            x.next()

if __name__ == "__main__":
    unittest.main()
