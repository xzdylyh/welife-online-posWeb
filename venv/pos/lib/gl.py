#_*_coding:utf-8_*_
import os,sys

global libPath
global reportPath #报告路径

PATH =lambda p:os.path.abspath(os.path.join(os.path.dirname(__file__),p))

'''全局变量'''
libPath = PATH(os.path.dirname(__file__)) #lib目录
reportPath = os.path.join(PATH(os.path.dirname(libPath)),'report')

if __name__=="__main__":
    print "lib路径:%s"%libPath
    print "report路径:%s"%reportPath