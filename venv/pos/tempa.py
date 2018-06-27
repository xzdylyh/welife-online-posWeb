#coding:utf-8
from requests import Session
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time,os
somelist = ['a','b','c','d','e','f','g','h']
print somelist[:]
print somelist[3:]
print somelist[3:5]
print somelist[3:-1]
print somelist[3:-2]
print somelist[-3:]
print somelist[-3:-1]
print somelist[-0:]
print somelist[0:]

print somelist[::-1]
print somelist[::2]
print somelist[1::2]
print somelist[::-2]

"""列表迭代,并取下标"""
for num,iter in enumerate(somelist):
    print '{0}:{1}'.format(num,iter)

for i in range(len(somelist)):
    print '{0}:{1}'.format(i,somelist[i])

"""数组是否为空判断"""
if somelist:
    print True
else:
    print False

if len(somelist)==0:
    print True
else:
    print False

"""列表推导式"""
list = [x +'a' for x in somelist]
print list

list = [x +'a' for x in somelist if x == 'c']
print list

url = 'http://boss.beta.acewill.net/captcha'
session = Session()
session.get(url)

login_url = 'http://boss.beta.acewill.net/user/login'
data = {"captcha":"2ema","password":"baihongye","username":"bhy@acewill.cn","refer":""}
res = session.post(login_url,data=data)
#print res.content

timestrac = int(time.time())
print timestrac

dirpath = r'D:\posWeb\venv\pos\report\images'

def rmDirsAndFiles(dirpath):
    """
    删除目标,目录下文件及文件夹
    :param dirpath: 目标目录
    :return: 无
    """
    listdir = os.listdir(dirpath)
    for f in listdir:
        filepath = os.path.join(dirpath,f)
        if os.path.isfile(filepath):
            os.remove(filepath)
        if os.path.isdir(filepath):
            os.rmdir(filepath)


rmDirsAndFiles(dirpath)


def switch_frame(self,*loc):
    """
    切换frame
    :param loc: 定位器
    :return: 无
    """
    try:
        element = self.driver.find_element(*loc)
        self.driver.switch_to.default_content()
        self.driver.switch_to.frame(element)
    except NoSuchElementException as ex:
        raise
