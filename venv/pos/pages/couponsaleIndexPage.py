#coding=utf-8
from pos.base import basepage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from pos.lib import scripts,gl
import time,os


class CouponsaleIndexPage(basepage.BasePage):
    '''商品售卖模块'''
    #定位器
    shop_phone_loc = (By.ID,'charge_number') #卡号或手机号
    shop_phoneBtn_loc = (By.XPATH,'/html/body/div[1]/div/div/div/div[2]/div[1]/div/div/button')#确定按钮
    """商品售卖页面"""
    shop_select_loc = (By.CLASS_NAME,'checkbox-inline') #商口复选择框
    shop_Num_loc = (By.NAME,'num') #数量输入框
    shop_confirmBtn_loc = (By.ID,'sell-submit') #确定按钮


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
    def assertShopSuccess(self):
        '''断言售卖成功'''
        resultBool = self.isExist(*(self.shop_phone_loc))
        print '返回到输入卡号界面?{0}'.format(resultBool)
        return resultBool




if __name__=="__main__":
    pass