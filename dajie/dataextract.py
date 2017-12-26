#coding:utf-8

import pymysql

class Data_extract:
    #封装基本的增和查
    def __init__(self):
        self.host = '127.0.0.1'
        self.database = 'spider'
        self.username = 'root'
        self.password = '123456'
        self.conn = None

    def SetCon(self):
        #获取数据库连接
        try:
            conn = pymysql.connect(self.host,self.username,self.password,self.database,charset='utf8mb4',)
            self.conn = conn
        except Exception as e:
            print('Error:',e)

    def Select(self,sql):
        #执行sql查询
        cursor = self.conn.cursor()
        count = cursor.execute(sql)
        fc = cursor.fetchall()
        return fc

    def Execute(self,sql):
        cursor = self.conn.cursor()
        try:
            cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            print('Something Wrong when insert:',e)
            with open('log.txt','a+') as f:
                f.write('Something Wrong when insert')
            self.conn.rollback()

    def Close(self):
        self.conn.close()