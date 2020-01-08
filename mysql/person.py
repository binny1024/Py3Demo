# -*- coding: utf-8 -*-
# @Time : 2020/1/8 16:00
# @Author : xubinbin
import pymysql

conn = pymysql.connect(
    host='localhost',
    user='root',
    passwd='liux1228',
    db='pydb',
    port=3306,
    charset='utf8'
)
executor = conn.cursor()
executor.execute("insert into persons (name, sex) values( %s , %s  );", ('张三', '1'))
conn.close()
