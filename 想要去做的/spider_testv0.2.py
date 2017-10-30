#coding:utf-8

from lxml import etree
import Bloomfilter
import requests
import urlparse
import os
import sys
'''
还缺什么 
1、Mongodb或Redis 存储
2、多线程
3、分布式
4、应对反爬虫机制 如脏数据 验证码 封ip等
'''

'''
属性:
    当前页面所有url
    下一级可爬url
    当前页面图片
    去重用的布隆过滤器
函数:
    Getcontent(self,url) 
        return the content of the website,using method get
    
    Get_url_list(self,content=self.Getcontent(self.url),paser=u'//body//a')
        return the url which can continue spider

    Recorrect_url()

    Download_picture(self,paser=u'//body//img')
        Download the picture of the url and then delete the url from list_url



'''
#print urlparse.urlparse(url)
#scheme='http', netloc='www.meizitu.com', path='/s/123.html', params='', query='', fragment=''

class Spider():

    def __init__(self):
        self.url = 'http://www.meizitu.com/'#当前的url
        self.domain = 'www.meizitu.com'#域名
       # self.urls = []#当前页面所有的url
        self.list_url = []#下一级可爬url
        self.list_picture = []#当前页面的图片
        self.bloomfilter = Bloomfilter.BloomFilter()#手写的布隆过滤器,去重用

    def Getcontent(sefl,url):
        #获取当前页面的内容
        Session = requests.session()
        return Session.get(url).content

    def Get_url_list(self,paser=u'//body//a'):
        #返回当前页面的所有非图片链接
        content=self.Getcontent(self.url)
        page = etree.HTML(content)
        tag = page.xpath(paser)
        urls = []
        for i in tag:
            urls.append(i.get('href'))
        return urls

    def Get_all_list(self,paser=u'//body//img'):
        #返回当前页面所有的链接
        content=self.Getcontent(self.url)
        page = etree.HTML(content)
        tag = page.xpath(paser)
        pics = []
        for i in tag:
            pics.append(i.get('src'))
        return self.Get_url_list()+pics
        
    #def Recorrect_url(*urls,*list_url,*list_picture):
    def  Recorrect_url(self):
        #将本页面所有的url去重后写入各自该存在的列表
        urls=self.Get_all_list()
        #print urls
        for url in urls:
            urlp = urlparse.urlparse(url)
            if not self.bloomfilter.isContains(url):
                self.bloomfilter.insert(url)
                if urlp.path.endswith('jpg'):
                    self.list_picture.append(url)
                elif urlp.netloc == self.domain:
                    self.list_url.append(url)
            

    def Download(self):
        #将该页面的图片下载，之后进入另一个url
        try:
            print 'HAHA'
            while self.list_picture is not None:
                print 'HAHA'
                url = self.list_picture.pop()
                print 'HAHA'
                with open('images/{}'.format(urlparse.urlparse(url).path.repladce('/','_')[-8:]),'wb+') as f:
                    f.write(Getcontent(url))
                    f.close()
        except:
            print 'Pop error,Please check whether list is null'
            return False
        

if __name__ == '__main__':
    if not os.path.exists('images'):
        os.mkdir('images')
    spider = Spider()
    try:
        while True:
            spider.Recorrect_url()
            print spider.list_url
            print '------************-------'
            print spider.list_picture
            spider.Download()
            if spider.list_url is not None:
                spider.url = spider.list_url.pop()
            else:
                print 'All is down'
                sys.exit(0)
    except:
        print 'Something wrong when running'