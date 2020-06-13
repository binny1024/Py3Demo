# -*- coding: utf-8 -*-
# @Time : 2020/1/3 16:39
# @Author : xubinbin
import collections
import json
from pprint import pprint

json_str = """
      
[
    {
        "name":"binny",
        "age":59
    },
    {
        "name":"binny",
        "age":59
    },
    {
        "name":"binny",
        "age":59
    }
]
"""
# json_list = json.loads(json_str)
# pprint(json_list)
# json_map = collections.defaultdict(list)
# for i in json_list:
#     pprint(i)
#     pprint(type(i))
# json_map[]
# print(json_map['age'])
# j2 = json.dumps(json_str)
# print(type (j2))
# json_map = collections.defaultdict(json_list)
# print(type(json_map))
# for i in json_map:
#     print(json_map[i])


# s = [('yellow', 1, 'r'), ('blue', 2,'r'), ('yellow', 3,'r'), ('blue', 4,'r'), ('red', 1,'r')]
# d = collections.defaultdict(list)
# for k, v, r in s:
#     print(r)
    # d[k].append(v)
# a = sorted(d.items())
# print(a)
gps = {}
print('len',len(gps))

