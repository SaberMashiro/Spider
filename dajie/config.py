class Config_var:
    def __init__(self):
        self.HEADERS = {
            'Host': 'm.dajie.com',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Trident/7.0; rv:11.0) like Gecko',
            'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'DNT':'1',
            'Connection': 'close',
        }
        self.COOKIES ={
            'DJ_RF':'empty',
            'DJ_EU':'http%3A%2F%2Fm.dajie.com%2Fsearch%2Fmore%3Fkeyword%3Dpython%26positionFunction%3D%26recruitType%3D%26city%3D%26salary%3D%26experience%3D%26page%3D1',
            'DJ_UVID':'MTUxNDE4OTU4ODg0MDgwNTYz' ,
            'aliyungf_tc':'AQAAAPgGnQgyvAwAWv3Q3TLNvfxLvcmV',
        }

    def SetHeaders(self,headers):
        self.HEADERS = headers
        
    def SetCookies(self,cookies):
        self.COOKIES = cookies

    def GetHeaders(self):
        return self.HEADERS

    def GetCookies(self):
        return self.COOKIES
        


