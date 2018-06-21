#coding:utf-8
import requests
usrstr = 'http://124.243.205.129/rest/n/feed/hot?appver=5.7.5.508&did=EB3C5966-C50E-432D-801E-D7EB42964654&c=a&ver=5.7&sys=ios9.3.5&mod=iPhone7%2C2&net=%E4%B8%AD%E5%9B%BD%E7%A7%BB%E5%8A%A8_5'
datadict={"":""}
res = requests.post(url=usrstr,data={})
print res.text

