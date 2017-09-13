import urllib.request as request
import random, redis, threading
import ctypes
import os
import platform
import sys

client = redis.StrictRedis("localhost", 6379)

def disk(folder):
    if platform.system() == 'Windows':
        free_bytes = ctypes.c_ulonglong(0)
        ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(folder), None, None, ctypes.pointer(free_bytes))
        return free_bytes.value/1024/1024/1024 
    else:
        st = os.statvfs(folder)
        return st.f_bavail * st.f_frsize/1024/1024

def download(url):
    randIP = str(random.randint(0, 255)) + "." + str(random.randint(0,255)) + "." + str(random.randint(0,255)) + "." + str(random.randint(0,255))
    req = request.Request(url)
    req.add_header('User-Agent', "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0")
    req.add_header('X-Forwarded-For', randIP)
    response = request.urlopen(req)
    file_size = int(response.getheader("Content-Length"))
    bytes_received = 0
    dir = "e:/test/"
    # 小于2g
    if disk("e:") <= 2048:
    	dir = "d:/test/"

    try:
        with open(dir + str(random.randint(1, 99999999999999999999)) + ".mp4", 'wb') as dst_file:
            while bytes_received / file_size != 1:
                _buffer = response.read(1024 * 1024)

                bytes_received += len(_buffer)
                dst_file.write(_buffer)
                print(threading.current_thread().name + " 已下载 " +  str(bytes_received / file_size))

    except KeyboardInterrupt:
        raise KeyboardInterrupt(
            "Interrupt signal given. Deleting incomplete video.")

def enter(**kwargs):
	start = kwargs["start"]
	end = kwargs["end"]

	for t in range(start, end):
		lst = client.lrange("91_src", start, end)
		for a in lst:
			src = a.decode("utf-8")
			download(src)
			print(threading.current_thread().name, " 下载 ", src, " 完成， 从redis 删除")
			client.lrem("91_src", 1, src)

if __name__ == "__main__":
	# thread_list = []

	# for i in range(1, 6):
	# 	start = (i - 1) * 4000 + 1
	# 	end = i * 4000 + 1
	# 	t = threading.Thread(target=enter, name="a" + str(i),kwargs={'start':start, 'end':end})
	# 	thread_list.append(t)

	# for t in thread_list:
	# 	t.start()

	# for t in thread_list:
	# 	t.join()

	# print("over")
	enter(start=1, end=2)