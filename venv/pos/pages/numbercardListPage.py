#coding:utf-8
from pos.base import basepage
from selenium.webdriver.common.by import By
from pos.lib import scripts,gl
import time,os

class NumberCardListPage(basepage.BasePage):
    """交易流水模块-次卡消费撤销"""
    """定位器"""
    list_undoLink_loc = (By.XPATH,'//*[@id="giftRunWater"]/table/tbody/tr[1]/td[7]') #撤销消费链接
    list_confirmBtn_loc = (By.ID,'cancelCost') #确认按钮
    list_assert_loc = (By.XPATH,'//*[@id="giftRunWater"]/table/tbody/tr[1]/td[5]/span/span') #新增一条交易类型为撤销消费


    """操作"""
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
    def assertSuccess(self):
        """断言,撤销消费成功"""
        print '断言:交易流水,新增一条,交易类型为撤销消费的记录'
        return self.isOrNoExist(*(self.list_assert_loc))