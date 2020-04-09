# Python操作数据库进行update时没有更新成功的问题
```python
import pymysql, os, configparser
sql_usr = 'aaa'
sql_psw = 'aaa'
sql_host = 'aaa'
sql_port = 'aaa'
 
def mysql1(sql):
    #打开数据库连接
    connection = pymysql.connect(host = sql_host,
                                 port = int(sql_port),
                                 user = sql_usr,
                                 password = sql_psw,
                                 charset = 'utf8')
    #使用cursor()方法创建一个游标对象cursor
    cursor = connection.cursor()
    cursor.execute(sql)#执行sql语句
    connection.commit()#执行update操作时需要写这个，否则就会更新不成功
    result = cursor.fetchone()
    #print(result)
    #result_cn = json.dumps(result,ensure_ascii=False)
    #print(result_cn)
    connection.close()
    return result
```
也就是说，如果要进行更新的操作，那么必须要在执行完sql后，加上`connection.commit()`,如果只是查询的话，那就不用加了。