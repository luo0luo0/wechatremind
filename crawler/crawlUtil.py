#coding: utf-8

import os

import mysql.connector
import requests

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36",
    "Connection": "keep-alive",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8" 
}

class ConvertibleBondStore():
    INSERT_CMD = "REPLACE INTO convertible_bond(id, code, title, description, start) VALUES('{id}', '{code}', '{title}', '{description}', '{start}')"

    def __init__(self):
        self._connection = mysql.connector.connect(
            host="localhost",
            user="root",
            db="calendar",
            password=os.getenv("MYSQL_PW"),
            charset="utf8",
            use_unicode=True
        )
    
    def put(self, bond):
        cmd = self.INSERT_CMD.format(**bond)
        print(cmd)
        db_cursor = self._connection.cursor()
        db_cursor.execute(cmd)
        self._connection.commit()
        
def parse_url(url):
    '''
    Sample:
    [{"id":"CNV5314","code":"127012","title":"【开始转股】招路转债","start":"2019-09-30","description":"转债代码:127012<br>转股代码:127012"}, ...]
    '''
    try:
        r = requests.get(url, headers=headers, timeout=5)
        return r.json()
    except Exception as e:
        print(e)
        return None

if __name__ == '__main__':
    print(parse_url('https://www.jisilu.cn/data/calendar/get_calendar_data/?qtype=CNV&start=1569772800&end=1573401600&_=1571313035898'))
