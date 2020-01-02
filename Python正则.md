### search 获取正则匹配出来的结果
```
search = re.search(r' (\w+) (\w+)', 'I Love Python')
print(search)
```
结果：<_sre.SRE_Match object; span=(1, 13), match=' Love Python'>
```
group = search.group()
print(group)
```
结果： Love Python
```
print(search.group(0))
```
结果： Love Python
```
print(search.group(1))
```
结果：Love
```
print(search.group(2))
```
结果：Python
```
print(search.start())
```
结果：1
```
print(search.end())
```
结果：13
```
print(search.span())
```
结果：(1, 13)
