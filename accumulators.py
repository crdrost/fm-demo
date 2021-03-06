import itertools

'''
An `accumulator` adds some push-based stream semantics to Python iterators,
which are pull-based (they do stuff when you ask for values, not when data is
available). To do this we define an accumulator as a function from iterators to
iterators, where the output iterator will make exactly one request to the input
iterator before yielding. This allows us to run multiple accumulators on one
input stream without having to buffer the whole list in memory, which is the
`batch` function below: all of the accumulators are run one step, then the cycle
continues again. It also lets us filter the calls to one accumulator based on a
predicate function while still ensuring that it does not get ahead of the batch,
this is the `prefilter` function. Finally `premap` takes an accumulator and
returns another accumulator which transforms the input stream by mapping it
before acting on it.
'''

def batch(*accs):
    '''Batch together all of the accumulators `*accs` so that they all act on a
    single iterator.'''
    def out(iterator):
        copies = itertools.tee(iterator, len(accs) + 1)
        result_streams = tuple(a(c) for (a, c) in itertools.izip(accs, copies))
        for i in copies[-1]:
            yield tuple(stream.next() for stream in result_streams)
    return out

def prefilter(predicate, acc):
    '''Filter the input to an accumulator based on whether it satisfies the
    predicate.'''
    def out(iterator):
        (i1, i2) = itertools.tee(iterator, 2)
        output = acc(itertools.ifilter(predicate, i2))
        last = None
        for i in i1:
            # There's a way to write this without duplicating the check but this
            # just looks so much cleaner.
            if predicate(i):
                last = output.next()
            yield last
    return out

def premap(fn, acc):
    '''Map the inputs to this accumulator with the given function before applying
    it to them.'''
    return lambda iterator: acc(itertools.imap(fn, iterator))

def count(iterator):
    '''Count the number of items in the iterator.'''
    c = 0
    for item in iterator:
        c += 1
        yield c

def unique(iterator):
    '''Count the number of unique items in the iterator.'''
    s = set()
    for item in iterator:
        s.add(item)
        yield len(s)

def grouped_count(iterator):
    '''Create a dictionary of the counts of how many times each value is seen in the iterator.'''
    d = dict()
    for item in iterator:
        d[item] = d.get(item, 0) + 1
        yield d

def scanning(fn):
    '''Scan across the iterator with the given function. The output stream will
    be `b[0] = a[0]`, `b[1] = fn(b[0], a[1])`, `b[2] = fn(b[1], a[0])`, and so 
    forth. In other words, this is `scanl1` from Haskell.'''
    def out(iterator):
        is_set = False
        value = None
        for item in iterator:
            if not is_set:
                value = item
                is_set = True
            else:
                value = fn(value, item)
            yield value
    return out
