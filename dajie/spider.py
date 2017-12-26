#coding:utf-8

import requests
import json
import threading
import queue
import datetime

import config
import dataextract



#请求=>解析=>存储
#请求部分I/O密集型使用多线程

url_and_response_queue = queue.Queue()#存放要请求的url
content_list_queue = queue.Queue()#第一次解析后得到存储数据的列表 
content_queue = queue.Queue()#第二次解析后得到的数据


dataextract = dataextract.Data_extract() #数据存储类
dataextract.SetCon()
var = config.Config_var()  #全局变量
headers = var.GetHeaders()
cookies = var.GetCookies()

now = str(datetime.datetime.now())#当前时间

def add_url_queue():
    #要爬的url
    for i in range(1,39):
        url = 'https://m.dajie.com/search/more?keyword=python&positionFunction=&recruitType=&city=&salary=&experience=&page={}'.format(i)
        url_and_response_queue.put(url)

def add_content_list_queue():
    #get请求，多线程
    try:
        url = url_and_response_queue.get()
        session = requests.session()
        content = session.get(url,headers=headers,cookies=cookies).content
        data = json.loads(content)
        content_list_queue.put(data['data']['list'])
    except Exception as e:
        print('Something Wrong when HttpGet:',e)
        with open('log.txt','a+') as f:
            f.write(now+'Something Wrong when HttpGet\n')


def add_content_queue():
    #将第一次解析后得到的列表进行再解析。
    #第一次解析的结果为列表，列表的每一项是一个字典，字典中存储着要存储解析的数据
    #第二次解析将列表变为字典
    try:
        for i in range(content_list_queue.qsize()):
            content_list = content_list_queue.get()
            for i in content_list:
                content_queue.put(i)
    except Exception as e:
        print('Somethis Wrong when extract twice:',e)
        with open('log.txt','a+') as f:
            f.write(now+'Somethis Wrong when extract twice\n')

def data_store():
    #content的key和value详见test.py
    #测试成功
    try:
        content = content_queue.get()

        title = content.setdefault('title',None)#工作名称
        corp = content.setdefault('corp',None)#公司名称
        salary = content.setdefault('salary',None)#薪水
        url = content.setdefault('url',None)#工作详情url
        url = 'http://m.dajie.com' + url
        keywords = content.setdefault('keywords',None)#列表,储存工作要求

        position = keywords[0]#工作地点
        year = keywords[1]#要求工作经验
        education = keywords[2]#学历
        other = ''.join(keywords)#所有需求

        sql = "insert into message(`title`,`corp`,`salary`,`url`,`position`,`year`,`education`,`other`)  values('%s','%s','%s','%s','%s','%s','%s','%s')" %(title,corp,salary,url,position,year,education,other)
        dataextract.Execute(sql)
    except Exception as e:
        print('Something Wrong When data_store,but dont worry:',e)
        with open('log.txt','a+') as f:
            f.write(now+'Something Wrong When data_store,but dont worry\n')

class V_Thread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        add_content_list_queue()


if __name__ == '__main__':
    with open('log.txt','a+') as f:
        f.write(now+'日志开始'+'\n')
    add_url_queue()
    thread_num = url_and_response_queue.qsize()
    threads = []

    for t in range(thread_num):
        thread = V_Thread()
        thread.start()
        threads.append(thread)

    for t in threads:
        t.join()
    add_content_queue()

    content_num = content_queue.qsize()
    for i in range(content_num):
        data_store()


