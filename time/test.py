import time
print(time.time())#获当前时间的时间戳
print(time.localtime())#获取本地时间
print(time.strftime('%Y-%m-%d',time.localtime()))#时间格式化



import calendar
import time
ts = calendar.timegm(time.gmtime())
print(ts)