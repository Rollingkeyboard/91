# -*- coding: UTF-8 -*-
import requests, re, redis, redisutil, time, random
from pyquery import PyQuery as pq
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
import threading
import common

# 将列表页插入redis
def parse(url, c):
    d = pq(common.visit(url))
    src = d("video").find("source").attr("src")
    if src != None:
    	print( threading.current_thread().name,  " insert into redis ", src)
    	redisutil.add(src, common.KEY_SRC)
    	c.lrem(common.KEY, 1, url)
    else:
    	print(threading.current_thread().name,  src, "解析为None, 插入 redis_error")
    	redisutil.add(src, common.KEY_NONE)

def enter(**kwargs):
    start = kwargs["start"]
    end = kwargs["end"]
    c = redisutil.connect()
    lst = c.lrange(common.KEY, int(start), int(end))

    for a in lst:
         print(threading.current_thread().name,  " parsing url ", a)
         parse(a, c)
         time.sleep(0.1)
    with open(common.PARSE_LOG, "a") as f:
        f.write(threading.current_thread().name + " 已经解析完毕.\n")

def start():
    thread_list = []
    total = redisutil.total(common.KEY   )
    page_size = 0
    thread_total = 5

    if total <= 5:
    	page_size = 1
    	thread_total = total
    else:
    	page_size = total / 5

    for t in range(1, thread_total + 1):
        start = (t - 1) * page_size + 1
        end = t * page_size + 1
        name = "a" + str(t)
        t = threading.Thread(target=enter, name=name, kwargs={"start":start, "end":end})
        thread_list.append(t)

    for t in thread_list:
    	t.start()

    for t in thread_list:
    	t.join()

    print("all thread over")