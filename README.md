# fm-demo
This is a demo application to show off my Python coding quirks; I tried to
follow a policy of "commit often" in case you wanted to also see the "way" I
program; it's very much "come up with some preprocessing steps; come up with a
strategy to make the algorithm obvious; write tests for those and then write the
algorithms which make the tests work; finally, write the algorithm in terms of
that language you've created."

In this case I decided up-front that I wanted each summary statistic to have its
own self-contained logic, but I wanted to run them all on the data set with 
*only constant memory usage overhead*. In a very early draft of accumulators.py 
you can see a first approach to this, but I slept on it and then realized that 
all of the components needed would look clearer if written in a Python generator
syntax.

To save GitHub some server storage I did not commit the CSV that you sent me,
but here is the result I get from running this program on that CSV:

    ┌« crdrost@perch:~/Desktop/fm-demo »
    └─ python main.py gps_can_data.csv
    Total GPS messages:  63843
    Total CAN messages:  1099032
    Unique CAN IDs:      61
    Time span covered:   20:34:58
    Average CANs/sec:    14.832141
    Average CANs/GPS:    17.214605
    Most CANs seen at:   2016-10-28 11:51:28
    Least CANs seen at:  2016-10-28 08:56:35

That is also how you use this: `python path/to/main.py path/to/data.csv`. There
are intentionally no dependencies on other packages that aren't vanilla Python.

This was a fun challenge, thanks!

# Code structure

The program is run from `main.py` which contains definitions for a bunch of 
stream-transformers that I am calling *accumulators*. When written in the right
language each one is more or less a one-liner; getting the maximum timestamp is
done by the `scanning(max)` transformer, but its input needs to first be mapped
to the actual timestamp and that is done by the `premap(timestamp, ____)`
function that encloses it. Finally the code says "If I am running this as a 
program, then read the CSV file and send it through the `csv` lib, and then
through two preformatters defined in `stream.py`, then run this batch of 
accumulators on it, then get the last row that those accumulators emit." Based
on those accumulated values we print the summary statistics requested. 

Finally there is a test suite for `stream.py` and `accumulators.py` that is
named just `test.py` and can be run as `python test.py`. It does not cover
main.py because I don't really have a bunch of real test data to run on it or
any corner-cases to watch out for here, that I know of.
