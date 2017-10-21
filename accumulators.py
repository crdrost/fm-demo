
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
