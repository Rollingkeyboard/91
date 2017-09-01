import requests, re, redisutil, time, random, threading
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

URL = "http://91.91p17.space/"
KEY = "91"

cookies = requests.cookies.RequestsCookieJar()
cookies.set("language", "cn_CN", domain=".91.91p17.space", path="/")


# 将列表页插入redis
def parseList(url):
    randomIP = str(random.randint(0, 255)) + "." + str(random.randint(0,255)) + "." + str(random.randint(0,255)) + "." + str(random.randint(0,255))
    retries = Retry(total=5,backoff_factor=10, status_forcelist=[500,502,503,504])
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0',
        'X-Forwarded-For': randomIP}
    s = requests.Session()
    s.mount('http://', HTTPAdapter(max_retries=retries))
    r = s.get(url, headers=headers, cookies=cookies)
    lst = re.compile(r'http:\/\/91\.91p17\.space\/view_video\.php\?viewkey\=\w+').findall(r.text)
    for a in set(lst):
        if not redisutil.exists(a, KEY):
            redisutil.add(a, KEY)
        else:
            print(threading.current_thread().name, " redis 已经存在，不再访问 ", a)

def enter(**kwargs):
    start = kwargs["start"]
    end = kwargs["end"]
    for page in range(start, end):
        url = "http://91.91p17.space/v.php?next=watch&page=" + str(page)
        try:
            print(threading.current_thread().name, " 解析 ", page, " 页 ", url)
            parseList(url)
            time.sleep(random.randint(1, 3))
        except RuntimeError:
            print(threading.current_thread().name, " visiting page ", page, " occurs some errors ", RuntimeError.__with_traceback__)
            redisutil.add(url, "91_error")
            continue
    with open("e:/test.log", "a") as f:
    	f.write(threading.current_thread().name + " over \n")

if __name__ == "__main__": 
    thread_list = []
    for i in range(1, 5):
        start = (i - 1) * 990 + 1
        end = i * 990 + 1
        name = "a" + str(i)
        t = threading.Thread(target=enter, name=name, kwargs={"start":start,"end":end})
        thread_list.append(t)

    for t in thread_list:
        t.start()

    for t in thread_list:
        t.join()
		
    print("all thread over")
