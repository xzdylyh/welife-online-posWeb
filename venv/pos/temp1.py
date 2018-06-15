#coding=utf-8
from selenium import webdriver
import time
"""
1.通过cookies跳过登录
2.线性脚本写一个积分兑换
3.添加断言
4.定义类，方法，进行简单封装
5.习惯性给重要步骤及函数添加注释
6.注意单引号和双引号的区别
7.三引号（单三引号和双三引号）
8.time.sleep()
"""
CONST_URL ="http://pos.beta.acewill.net/credit" #积分换礼页面url

driver = webdriver.Chrome()  #创建webdriver实例
driver.maximize_window() #最大化浏览器
driver.get(CONST_URL) #打开指定url
"""
driver.implicitly_wait(30) 智能等待30秒
所谓智能等待，在指定时间内页面加载完成
即不在等待。
"""
driver.implicitly_wait(30)

"""
定位元素的八种方法X2：
1.driver.find_element_by_id  通过id来定位
2.driver.find_element_by_xpath 通过xpath来定位
3.driver.find_elements_by_name 通过name来定位
4.driver.find_element_by_tag_name 通过标签来定位
5.driver.find_element_by_class_name 通过class属性名来定位
6.driver.find_element_by_link_text 通过链接文本来定位
7.driver.find_element_by_css_selector 通过css来定位
8.driver.find_element_by_partial_link_text 通过部分链接文本来定位
"""
"""
解释：
ID定位: html标签唯一标识 <input type="button" id ="confirm_login"/>
XPATH定位: 通过html标签树型结构，层层定位,一般用于元素没有id name等唯一标识
    <html>
       <head></head>
       <body>
            <div class="col-lg-3" id="main_div">
                <div class="login">
                    <input type="text" value>输入用户名</input>
                    <input type="text" value>输入密码</input>
                    <input type="button">登录</input>
                <div>
                <div>
                    <p>请输入用户名及密码，点击登录</p>
                </div>
                
            <div> 
       </body>
    </html>
如上，用户名，密码，登录按钮，都没有id，name等唯一标识
那么对于这种定位，可以使用XPATH  css等进行定位
例上边用户名定位：展示两种方法
driver.find_elements_by_xpath("/html/body/div[1]/div[1]/input[1]") #用户名
driver.find_elements_by_xpath("//div[@id='main_div']/div[1]/input[1]")

NAME定位:标签唯一标识name属性值
tag Name定位：通过标签名定位
class name定位：标签class属性值来定位，值得注意的是通过html标签class属性值有多个,以空格分开。取其一使用即可。
       例：<div class="button input xxxx">....</div>

link text定位：有一些链接没有id name，可以通过文本来定位，当然xpath都可以。定位方法可以灵活使用。
       例:<a href="/xxx/xxx">提交</a> 可以通过找提交这个文本

partial_link_text 定位：有一些链接如果很长，或有部分是动态的。此方法正合适。
       例:<a href="/xxx/xxx">提交xxx12fdscxv8j93k9j我是动d态的</a>  提交是固定的，可以找提交
"""

"""跳过登录，向浏览器写cookies信息"""
"""
"""

cookinfo1 = {"name":"pos_entry_number","value":"1003935039186461"}
cookinfo2 = {"name":"pos_entry_actualcard","value":"1003935039186461"}
cookinfo3 = {"name":"pos_bid","value":"2048695606"}
cookinfo4 = {"name":"pos_mid","value":"1234871385"}
cookinfo5 = {"name":"pos_sid","value":"1512995661"}
cookinfo6 = {"name":"pos_sign","value":"369240630d5e17a24bf7e5a70f073465"}

"""cookies增加到浏览器，注意这个要在driver.get()之后增加，才能准备到将cookies写入打开的网址"""
driver.add_cookie(cookinfo1)
driver.add_cookie(cookinfo2)
driver.add_cookie(cookinfo3)
driver.add_cookie(cookinfo4)
driver.add_cookie(cookinfo5)
driver.add_cookie(cookinfo6)

driver.get(CONST_URL) #写完cookies之后，要重新访问写入cookies的地址
driver.implicitly_wait(30) #智能等待加载完成

driver.find_element_by_id('charge_number').send_keys('1003935039186461') #输入卡号
driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div[2]/div[1]/div/div/button').click() #确定按钮

#driver.quit() #完成以后步骤后，关闭浏览器，释放driver实例
