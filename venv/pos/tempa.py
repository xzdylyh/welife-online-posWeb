#coding:utf-8
from requests import Session
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import time,os
import zipfile
from pos.lib import gl
'''
driver = webdriver.Chrome()
driver.maximize_window()
driver.get('https://www.baidu.com')
driver.implicitly_wait(30)

loc = (By.ID,'kw')
'''
def find_element(*loc):
    """
    查询元素
    :param loc: 定位器
    :return: 找到返回元素对象 否则返回 None
    """
    """时间设置(秒)"""
    timeout = 10 #超时时间
    poll_frequency = 0.5 #轮询间隔时间

    start_time = time.time().__int__()
    while True:
        try:
            element = driver.find_element(*loc)
            return element
        except NoSuchElementException as ex:
            if (time.time().__int__() - start_time) >timeout:
                return None
        time.sleep(poll_frequency)


a = r'd:\123'
b = ''

a = a and os.sep or b
print a

dirpath = gl.reportPath
outname = r'report.zip'
zip = zipfile.ZipFile(outname,"wb")
for path,dirnames,filenames in os.walk(dirpath):
    print 'path:{0}'.format(path)
    print 'dir:{0}'.format(dirnames)
    print 'file:{0}'.format(filenames)




def zip_ya(startdi,file_news):
    startdir = ".\\123"  #要压缩的文件夹路径
    file_news = startdir +'.zip' # 压缩后文件夹的名字
    z = zipfile.ZipFile(file_news,'w',zipfile.ZIP_DEFLATED) #参数一：文件夹名
    for dirpath, dirnames, filenames in os.walk(startdir):
        fpath = dirpath.replace(startdir,'') #这一句很重要，不replace的话，就从根目录开始复制
        fpath = fpath and fpath + os.sep or ''#这句话理解我也点郁闷，实现当前文件夹以及包含的所有文件的压缩
        for filename in filenames:
            z.write(os.path.join(dirpath, filename),fpath+filename)
            print ('压缩成功')
    z.close()

session = Session()
session.get('xxxxx')
res = session.post(url,data={xxxx})

