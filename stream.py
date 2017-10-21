
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

