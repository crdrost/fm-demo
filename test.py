import unittest
import stream
import datetime
import accumulators


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

def adder(n):
    def out(iterator):
        for i in iterator:
            yield i + n
    return out

class TestAccumulators(unittest.TestCase):
    def test_batch(self):
        acc = accumulators.batch(adder(3), adder(5))
        x = acc(xrange(4))
        self.assertEqual(x.next(), (3, 5))
        self.assertEqual(x.next(), (4, 6))
        self.assertEqual(x.next(), (5, 7))
        self.assertEqual(x.next(), (6, 8))
        with self.assertRaises(StopIteration):
            x.next()

    def test_prefilter(self):
        acc = accumulators.prefilter(lambda x: x % 3 == 1, adder(10))
        self.assertEqual(
            list(acc(xrange(10))),
            [None, 11, 11, 11, 14, 14, 14, 17, 17, 17]
        )

    def test_premap(self):
        acc = accumulators.premap(lambda x: x - 10, adder(10))
        self.assertEqual(
            list(acc(xrange(10))),
            range(10)
        )

    def test_prefilter(self):
        acc = accumulators.prefilter(lambda x: x % 3 == 1, adder(10))
        self.assertEqual(
            list(acc(xrange(10))),
            [None, 11, 11, 11, 14, 14, 14, 17, 17, 17]
        )

    def test_premap(self):
        acc = accumulators.premap(lambda x: x - 10, adder(10))
        self.assertEqual(
            list(acc(xrange(10))),
            range(10)
        )

    def test_count(self):
        self.assertEqual(
            list(accumulators.count(xrange(50, 500))),
            range(1, 451)
        )

    def test_unique(self):
        src = iter(
            ['apple','mango','apple','mango','orange','apple','orange','plum']
        )
        self.assertEqual(
            list(accumulators.unique(src)),
            [1, 2, 2, 2, 3, 3, 3, 4]
        )

    def test_grouped_count(self):
        src = accumulators.grouped_count(iter(
            ['apple','mango','apple','mango','orange','apple','orange','plum']
        ))
        self.assertEqual(src.next(), {'apple': 1})
        self.assertEqual(src.next(), {'apple': 1, 'mango': 1})
        self.assertEqual(src.next(), {'apple': 2, 'mango': 1})
        self.assertEqual(src.next(), {'apple': 2, 'mango': 2})
        self.assertEqual(src.next(), {'apple': 2, 'mango': 2, 'orange': 1})
        self.assertEqual(src.next(), {'apple': 3, 'mango': 2, 'orange': 1})
        self.assertEqual(src.next(), {'apple': 3, 'mango': 2, 'orange': 2})
        self.assertEqual(src.next(), {'apple': 3, 'mango': 2, 'orange': 2, 'plum': 1})

    def test_scanning(self):
        x = [7, 2, 5, 3, 6, 1, 8, 4, 0, 9]
        self.assertEqual(
            list(accumulators.scanning(min)(iter(x))),
            [7, 2, 2, 2, 2, 1, 1, 1, 0, 0]
        )
        x = [7, 2, 5, 3, 6, 1, 8, 4, 0, 9]
        self.assertEqual(
            list(accumulators.scanning(max)(iter(x))),
            [7, 7, 7, 7, 7, 7, 8, 8, 8, 9]
        )

if __name__ == "__main__":
    unittest.main()
