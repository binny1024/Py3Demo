import re

s = '中国平安 (000001)'

p = r'\d+'

ss = re.search(p, s)
print(ss.group())
p = "[^ (" + ss.group() + ")]+"
ss = re.search(p, s)
print(ss.group())
