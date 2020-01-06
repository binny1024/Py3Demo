# -*- coding: utf-8 -*-
# @Time : 2020/1/3 16:39
# @Author : xubinbin
import json

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
json_obj = json.loads(json_str)
for i in json_obj:
    print(json_obj[i])
