from datetime import timedelta, datetime
import redis
import sys

REDIS = redis.Redis(port= int(sys.argv[1]) if len(sys.argv) > 1 else 6379  )

today = datetime.now()

def items_generator():
    """
    Assuming that we want to store value ``i`` for item which has ``pk=i``
    """
    for i in xrange(15000):
        yield i


def days_generator():
    for i in xrange(12*5):
        yield (today + timedelta(days=30*i)).strftime('%Y-%m')


REDIS.flushall()
print "Start redis size:", REDIS.info()['used_memory_human']

print "Testing plain SET command",

with REDIS.pipeline(transaction=False) as pipe:
    for days in days_generator():
        for item in items_generator():
            pipe.set(days + '_item:' + str(item), item)
    pipe.execute()

print ', redis size =', REDIS.info()['used_memory_human']


print "Testing HINCRBY command (100 items buckets)",
REDIS.flushall()

with REDIS.pipeline(transaction=False) as pipe:
    for days in days_generator():
        for item in items_generator():
            # print days + '_bucket' + str(item / 100), str(item), item
            pipe.hincrby(days + '_bucket' + str(item / 100), str(item), item)
    pipe.execute()

print ', redis size =', REDIS.info()['used_memory_human']


print "Testing HINCRBY command (500 items buckets)",
REDIS.flushall()

with REDIS.pipeline(transaction=False) as pipe:
    for days in days_generator():
        for item in items_generator():
            # print days + '_bucket' + str(item / 100), str(item), item
            pipe.hincrby(days + '_bucket' + str(item / 500), str(item), item)
    pipe.execute()

print ', redis size =', REDIS.info()['used_memory_human']



print "Testing HINCRBY command (1000 items buckets)",
REDIS.flushall()

with REDIS.pipeline(transaction=False) as pipe:
    for days in days_generator():
        for item in items_generator():
            # print days + '_bucket' + str(item / 100), str(item), item
            pipe.hincrby(days + '_bucket' + str(item / 1000), str(item), item)
    pipe.execute()

print ', redis size =', REDIS.info()['used_memory_human']

