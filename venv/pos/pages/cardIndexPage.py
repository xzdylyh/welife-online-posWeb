#coding=utf-8
from pos.base import basepage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from pos.lib import scripts,gl
import time,os


class CardIndexPage(basepage.BasePage):
    '''储值卡售卖模块'''
    #定位器
    card_Select_loc = (By.NAME,'name') #选择卡

    card_Type_loc = (By.XPATH,'//*[@id="cardChoose"]/label[2]') #储值卡类型
    card_Numer_loc = (By.XPATH,'//*[@id="cardNum"]/div/ul/li/input') #储值卡号
    card_ConfirmBtn_loc = (By.XPATH,'//*[@id="cardBtn"]') #确定按钮
    card_toConfirmBtn_loc = (By.XPATH,'//*[@id="myModal"]/div/div/div/div/button[1]') #再次确定
    card_AssertSuccess_loc = (By.XPATH,'//*[@id="cardNum"]/div/ul/li/span') #断言储值卡已售卖


    #封装操作
    @property
    def open(self):
        yamldict = scripts.getYamlfield(os.path.join(gl.configPath, 'config.yaml'))
        ck_dict = yamldict['CONFIG']['Cookies']['LoginCookies']
        self._open(self.base_url,self.pagetitle)
        self.addCookies(ck_dict)
        self._open(self.base_url, self.pagetitle)

    @scripts.Replay
    def selectTab(self,*loc):
        '''选择tab操作'''
        self.find_element(*loc).click()

    @scripts.Replay
    def selectDownList(self,option=0,index=0,value=0,txt='',*loc):
        """选择下拉列表框"""
        element = self.find_element(*loc)
        ul = Select(element)
        if option==0:
            ul.select_by_index(index)
        elif option==1:
            ul.select_by_value(value)
        else:
            ul.select_by_visible_text(txt)



    @scripts.Replay
    def inputText(self,text,desc,*loc):
        '''输入文本操作'''
        print 'Input{0}:{1}'.format(desc,text)
        self.send_keys(text,*loc)


    @scripts.Replay
    def clickBtn(self,desc,*loc):
        '''点击操作'''
        print 'Click:{0}'.format(desc)
        self.wait(1000) #线程休眠1000毫秒
        self.find_element(*loc).click()


    @property
    def assertChareSuccess(self):
        '''断言支付成功'''
        self.getImage
        return self.getTagText('text',*(self.card_AssertSuccess_loc))





if __name__=="__main__":
    pass