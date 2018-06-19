#coding=utf-8

from selenium import webdriver
import time,json
timeStr = time.strftime('%Y-%m-%d')
print timeStr
phone = '13712345678'
url = 'http://boss.beta.acewill.net/sms/search?phone={0}&begin={1}&end={2}'.format(phone,timeStr,timeStr)
print url


class GetCode(object):
    def __init__(self):

        self.driver1 = webdriver.Chrome()

    def getCode(self):
        timeStr = time.strftime('%Y-%m-%d')
        print timeStr
        phone = '13712345678'
        url = 'http://boss.beta.acewill.net/sms/search?phone={0}&begin={1}&end={2}'.format(phone, timeStr, timeStr)
        print url
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get(url)
        self.driver.implicitly_wait(30)
        self.driver.add_cookie({"name":"UserSession","value":"5b28be4b3cdfb"})
        self.driver.get(url)

        txtcode = self.driver.find_element_by_xpath('//*[@id="example2"]/tbody/tr[1]/td[4]').text
        code = json.loads(txtcode)['template']['yanzhengma']
        print code
        self.driver.quit()
        return code

    def pos(self):

        url = "http://pos.beta.acewill.net/consume"
        self.driver1.maximize_window()
        self.driver1.get(url)

        LoginCookies= {"pos_entry_number": "1003935039186461",
                       "pos_entry_actualcard": "1003935039186461",
                       "pos_bid": "2048695606",
                       "pos_mid": "1151957379",
                       "pos_sid": "1512995661",
                       "pos_sign": "d0c5d8d04c71e1342cf8a632102dfe65"}

        for key in LoginCookies.keys():
            self.driver1.add_cookie({"name":key,"value":LoginCookies[key]})

        self.driver1.get(url)
        code = self.getCode()

        self.driver1.switch_to.window(self.driver1.current_window_handle)
        self.driver1.find_element_by_id('charge_number').send_keys(code)


if __name__=="__main__":
    GetCode().pos()

