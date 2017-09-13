import parse_list, parse_src, time

print("即将启动解析列表程序")
parse_list.start()

# 睡眠5分钟后启动
print("5分钟后将启动解析视频程序")
time.sleep(2)
parse_src.start()