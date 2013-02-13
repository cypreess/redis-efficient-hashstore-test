redis-efficient-hashstore-test
==============================

This test shows how efficiently store millions of key-values pairs in redis.

* The standard way is to store them using SET command.
* The tricky way is to use redis hash data type with bucketing.


Runing
------

```
$ pip install -r pip.req
$ python run_test.py [optional redis port]
```

Warning: THIS TEST WILL FLUSH YOUR REDIS!!! IT MEAN THAT WILL COMPLETELY DELETE REDIS CONTENT


Example
-------
Consider you need to keep something like statistics for some number of objects. Lets say you have 15k objects (identified by
plain int ids from 0 to 14999). Lets say you want for every object keep monthly stats (some number).

The standard way is to think of it as a big hash table with following keys:

```
2013-02_item0   : <some number>
2013-02_item1   : <some number>
2013-02_item2   : <some number>
2013-02_item3   : <some number>
...
2013-02_item14999 : <some number>
2013-03_item0   : <some number>
...
2013-04_item0   : <some number>
...
2013-05_item0   : <some number>
...
```

You get the point.

Storing this stats using redis SET command this way for a 5 years (5*12 months) will use:

```
Testing plain SET command , redis size = 76.24M
```

The smarter way is to store them using redis hash object. Redis can store very memory efficiently hash objects that
are smaller then some particular value (configured via ``hash-max-zipmap-entries``).

So the other aproach is to divide every day-item-stat into buckets (simply using trivial item_id/N division), just to be
sure that every bucket will not have more than N elements.

For example for N=10:

```
2013-02_bucket0     0      <some number>
2013-02_bucket0     1      <some number>
2013-02_bucket0     2      <some number>
...
2013-02_bucket0     9      <some number>
2013-02_bucket1    10      <some number>
2013-02_bucket1    11      <some number>
...
```


The number in the middle column is now just a raw item id number. This works like a charm:

```
Testing HINCRBY command (100 items buckets) , redis size = 11.52M
Testing HINCRBY command (500 items buckets) , redis size = 10.69M
Testing HINCRBY command (1000 items buckets) , redis size = 10.59M
```

This test was generated on 900 000 key-value pairs.


Comments
========
Krzysztof Dorosz <cypreess@gmail.com>