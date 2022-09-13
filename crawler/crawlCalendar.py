#coding: utf-8

import crawlUtil
import time, datetime

'''
功能：
   每天晚上（T），把最近10天的数据爬取下来[T+1,T+30）的可转债日历
'''
if __name__ == "__main__":
    today =  datetime.date.today()
    beginDate = today + datetime.timedelta(days=1)
    endDate = today + datetime.timedelta(days=30)
    beginDateStr = beginDate.strftime("%s")
    endDateStr = endDate.strftime("%s")
    requestURL = "https://www.jisilu.cn/data/calendar/get_calendar_data/?qtype=CNV&start={0}&end={1}&_={2}".format(beginDateStr, endDateStr, int(time.time()))
    print("==DEBUG==:request url:",requestURL)
    print("==DEBUG==:[beginDate,endDate]",str(beginDate),str(endDate))
    data = crawlUtil.parse_url(requestURL)
    store = crawlUtil.ConvertibleBondStore()
    for bond in data:
        store.put(bond)
