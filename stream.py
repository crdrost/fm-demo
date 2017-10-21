import datetime

def dicts_from_lists(rows):
    """
    Parse a stream of lists into a stream of dicts.

    The first list is used as a header row, i.e. it contains keys which will be
    indexes into the dictionaries. Every subsequent list is used as a data row.
    """
    rows = iter(rows)
    header = rows.next()
    cols = len(header)
    for row in rows:
        yield {header[i]: row[i] for i in range(cols)}

def gpscans_from_dicts(rows):
    """
    Parse a stream of rows into a stream of GPS/CAN tuples. Right now these are either

        ('can', ts, puc_id, (message_id, dlc, payload))

    or

        ('gps', ts, puc_id, (gps_id, latitude, longitude, groundspeed, truecourse))

    from the {'ts', 'puc_id', 'gps_id', 'message_id', ...} etc dictionary of rows.
    """
    for row in rows:
        ts = datetime.datetime.strptime(row['ts'], '%Y-%m-%d %H:%M:%S')
        puc_id = int(row['puc_id'])
        if row.get('message_id', '') != '':
            yield ('can', ts, puc_id,
                   (row['message_id'], int(row['dlc']), row['payload']))
        elif row.get('gps_id', '') != '':
            yield ('gps', ts, puc_id, (int(row['gps_id']),
                    float(row['latitude']), float(row['longitude']),
                    float(row['groundspeed']), float(row['truecourse'])))
        else:
            raise ValueError(
                'Row could not be identified as a "gps" or "can" row: %s' % repr(row)
            )
