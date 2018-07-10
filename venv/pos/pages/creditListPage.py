#coding:utf-8
from pos.base import basepage
from selenium.webdriver.common.by import By
from pos.lib import scripts,gl
import time,os

class CreditListPage(basepage.BasePage):
    """交易流水模块"""
    """定位器"""
    #交易流水-撤销积分
    undo_LinkBtn_loc = (By.XPATH,'//*[@id="giftRunWater"]/table/tbody/tr[1]/td[9]/span/a') #撤销积分链接
    undo_Btn_loc = (By.ID,'cancelGift') #确定按钮
    undo_assertList_loc = (By.XPATH,'//*[@id="giftRunWater"]/table/tbody/tr[1]/td[7]/span') #撤销积分后,交易列表增加一条状态,撤销积分换礼


    """操作"""

    #封装操作
    @property
    def open(self):
        yamldict = scripts.getYamlfield(os.path.join(gl.configPath, 'config.yaml'))
        ck_dict = yamldict['CONFIG']['Cookies']['LoginCookies']
        self._open(self.base_url,self.pagetitle)
        self.addCookies(ck_dict)
        #time.sleep(3)
        self._open(self.base_url, self.pagetitle)

    @scripts.Replay
    def selectTab(self,desc,*loc):
        '''选择tab操作'''
        print 'Select{0}:{1}'.format(desc,loc)
        self.find_element(*loc).click()

    @scripts.Replay
    def inputText(self,text,desc,*loc):
        '''输入文本操作'''
        print 'Input{0}:{1}'.format(desc,text)
        self.send_keys(text,*loc)


    @scripts.Replay
    def clickBtn(self,desc,*loc):
        '''单击操作'''
        print 'Click{0}:{1}'.format(desc,loc)
        self.find_element(*loc).click()

    @property
    def assertCancelSuccess(self):
        """断言,撤销成功"""
        text = self.find_element(*(self.undo_assertList_loc)).text
        self.getImage
        return text