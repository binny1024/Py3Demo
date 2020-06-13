# 判断字典里有没有某一个 key

AttributeError: 'dict' object has no attribute 'has_key'

has_key方法在python2中是可以使用的，在python3中删除了。

比如：
```python
dict ={}
if dict.has_key('word'):
    print()
```
改为：
```python
dict ={}
if 'word' in dict:
    print()
```

