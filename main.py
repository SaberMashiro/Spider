#-*-coding:utf-8-*-
#-*-Author:CMDY-*-
'''
这个py目标是能够自动遍历图片下载，而非上个版本的通过数字爆破
'''
import urllib2
import urllib
import StringIO
import re
import cookielib
import requests
import urlparse

'''
流程：   进入一个url==》得到url的content==》识别url外链和图片==》下载图片==》进入url_list的第一个页面并删除本身==》循环
'''

class Meizitu():
    def __init__(self):
        self.url = ''
        self.url_list = [] #用列表储存当前页面的所有url外链
        self.url_list_exist = [] #用列表来判别某url是否已经检测到过
        self.url_picture = []  #本页面中的图片
        self.url_picture_exist = [] #是否检测过的图片
        self.headers ={
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.114 Safari/537.36',
            'Cookie': '__jsluid=54d506fa7bd1d5ab966d0a8dbc1ba2c8',
            }
    def Getcontent(self):
        return requests.get(self.url,headers=self.headers).content

    def CheckUrl(self):
        self.url_list = re.findall(r'http://www.meizitu.com/a/.+?l', self.Getcontent())
        for i in self.url_list:
            if i not in self.url_list_exist:
                self.url_list_exist.append(i)
        self.url_picture = re.findall(r'src="(.+?\.jpg)"', self.Getcontent())
        for i in self.url_picture:
            if i not in self.url_picture_exist:
                self.url_picture_exist.append(i)

    def Download_Picture(self):
        for i in self.url_picture_exist:
            response = StringIO.StringIO(requests.get(i,headers=self.headers).content)
            with open('{}'.format(str(urlparse.urlsplit(i).path.replace("/","_"))),'wb') as f:
                f.write(response.getvalue())
                f.close()
        self.url = self.url_list_exist[0]
        del self.url_list_exist[0]



if __name__=='__main__':
    Meizitu = Meizitu()
    Meizitu.url = 'http://www.meizitu.com/'
    times = int(raw_input('Please input the url nums you want to spider:\n'))
    for i in xrange(0,times):
        Meizitu.CheckUrl()
        Meizitu.Download_Picture()
        #print Meizitu.url_list_exist
        #print Meizitu.url_picture
        #print type(Meizitu.url)

