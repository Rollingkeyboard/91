import redis

def connect():
    r = redis.StrictRedis(host="localhost", port=6379, db=0, decode_responses=True)
    return r

def setredis(url, key):
    r = connect()
    if not r.sismember(key, url):
        r.sadd(key, url)

def exists(url, key):
    r = connect()
    lst = r.lrange(key, 0, -1)
    flag = -1
    for a in lst:
        if a == url:
            flag = 1
            break
    if flag == 1:
        return True
    else:
        return False

def add(url, key):
    if not exists(url, key):
        r = connect()
        r.rpush(key, url)

def remove(url, key):
    if exists(url, key):
        r = connect()
        r.lrem(key, 0, url)