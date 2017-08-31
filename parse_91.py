import requests, re, redis, redisutil, time, random
from pyquery import PyQuery as pq 
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
import threading

URL = "http://91.91p17.space/"
KEY = "91_src"

cookies = requests.cookies.RequestsCookieJar()
cookies.set("watch_times", "1", domain="91.91p17.space", path="/")


# 将列表页插入redis
def parse(url, c):
    randomIP = str(random.randint(0, 255)) + "." + str(random.randint(0,255)) + "." + str(random.randint(0,255)) + "." + str(random.randint(0,255))
    retries = Retry(total=5,backoff_factor=10, status_forcelist=[500,502,503,504])
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0',
        'X-Forwarded-For': randomIP}
    s = requests.Session()
    s.mount('http://', HTTPAdapter(max_retries=retries))
    d = pq(s.get(url, headers=headers, cookies=cookies).text)
    src = d("video").find("source").attr("src")
    if src != None and not redisutil.exists(src, KEY):
    	print( threading.current_thread().name,  " insert into redis ", src)
    	redisutil.add(src, KEY)
    	c.lrem("91", 1, url)  
    else:
    	print(threading.current_thread().name,  src, "解析为None 或者 已经存在，不再访问")

def enter(**kwargs):
    start = kwargs["start"]
    end = kwargs["end"]
    c = redisutil.connect()
    lst = c.lrange("91", start, end)

    for a in lst:
         print(threading.current_thread().name,  " parsing url ", a)
         parse(a, c)
         time.sleep(random.randint(1, 3))

if __name__ == "__main__":
    thread_list = []
    for t in range(1, 6):
        start = (t - 1) * 15800 + 1
        end = t * 15800 + 1
        name = "a" + str(t)
        t = threading.Thread(target=enter, name=name, kwargs={"start":start, "end":end})
        thread_list.append(t)

    for t in thread_list:
    	t.start()

    for t in thread_list:
    	t.join()

    print("all thread over")