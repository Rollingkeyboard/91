# -*- coding: UTF-8 -*-
import redis, math, common

# 将每个视频的url写入文件，然后用迅雷拖吧
c = redis.StrictRedis("localhost", 6379)
lst = c.lrange("91_src", 0, -1)

total = len(lst)
count = math.floor(total / 1000) + 1 # 比如 3005个，需要4个文件，每个文件1000个，最后一个文件5个

for i in range(1, int(count + 1)):
	s = ""
	for a in lst[(i - 1) * 1000 : i * 1000]:
		src = a.decode("utf-8")
		if src != "None":
			s += src + "\n"
			c.lrem(common.KEY_SRC, 1, src)
			# print("remove from redis ", src)

	with open(common.TORRENT + "/" + str(i) + ".txt", 'a') as f:
		f.write(s)
	print("writing file ", i)