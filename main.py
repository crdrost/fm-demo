import csv
import accumulators as acc
import stream

def is_gps(gpscan):
    return gpscan[0] == 'gps'

def is_can(gpscan):
    return gpscan[0] == 'can'

def can_message_id((can, ts, puc, meta)):
    if can != 'can':
        raise ValueError("Tried to call can_message_id on a non-CAN data point.")
    return meta[0]

def timestamp(gpscan):
    return gpscan[1]

# accumulator to count GPS rows only
total_gps = acc.prefilter(is_gps, acc.count)

# accumulator to count CAN rows only
total_can = acc.prefilter(is_can, acc.count)

# accumulator to count unique CAN message_ids
unique_can = acc.prefilter(is_can, acc.premap(can_message_id, acc.unique))

min_timestamp = acc.premap(timestamp, acc.scanning(min))

max_timestamp = acc.premap(timestamp, acc.scanning(max))

can_counts_by_timestamp = acc.prefilter(is_can, acc.premap(timestamp, acc.grouped_count))

def just_the_last_row(iterator):
    last = None
    for item in iterator:
        last = item
    return last

def maybe(x, default):
    if x == None:
        return default
    return x

__usage__ = '''Usage: python fm-demo/main.py path/to/data.csv

Collects summary statistics about the data in data.csv and prints them out.
'''

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print __usage__

    with open(sys.argv[1]) as f:
        csv_rows = stream.dicts_from_lists(csv.reader(f))
        gpscans = stream.gpscans_from_dicts(csv_rows)
        raw_stats_accumulator = acc.batch(
            total_gps,
            total_can,
            unique_can,
            min_timestamp,
            max_timestamp,
            can_counts_by_timestamp
        )
        (g_tot, c_tot, c_uni, min_ts, max_ts, ts_counts) = just_the_last_row(
            raw_stats_accumulator(gpscans)
        )
        time_elapsed = max_ts - min_ts
        c_tot = maybe(c_tot, 0)
        print 'Total GPS messages:  %i' % maybe(g_tot, 0)
        print 'Total CAN messages:  %i' % c_tot
        print 'Unique CAN IDs:      %i' % maybe(c_uni, 0)
        print 'Time span covered:   %s' % time_elapsed
        print 'Average CANs/sec:    %f' % (c_tot / time_elapsed.total_seconds())
        print 'Average CANs/GPS:    %f' % (c_tot / float(g_tot))
        max_ts_count = max(ts_counts.values())
        first_max = min(ts for ts in ts_counts if ts_counts[ts] == max_ts_count)
        print 'Most CANs seen at:   %s' % first_max
        min_ts_count = min(ts_counts.values())
        first_min = min(ts for ts in ts_counts if ts_counts[ts] == min_ts_count)
        print 'Least CANs seen at:  %s' % first_min
