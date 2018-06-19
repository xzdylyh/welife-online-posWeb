#coding=utf-8
from selenium import webdriver
from selenium.webdriver.common.by import By
from pos.pages import creditPage
import unittest,ddt,os
from pos.lib import gl,HTMLTESTRunnerCN,scripts

creditData = [{"charge_number":"1003935039186461","ExchangeNumber":1,"ExchangeDetail":u"自动化测试大礼包1个","desc":u"正常积分兑换流程"}]

@ddt.ddt
class TestCreditPage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """初始化webdriver"""
        cls.driver = webdriver.Chrome()
        cls.url = 'http://pos.beta.acewill.net/credit'


    def creditFunc(self,data):
        '''输入卡号或手号并点击确定'''
        self.credit = creditPage.CreditPage(self.url,self.driver,u"积分换礼 - 微生活POS系统")
        self.credit.open  #增加cookies信息,并打开积分换礼页

        self.credit.inputText(data['charge_number'],"输入手机号或卡号",*(self.credit.charge_number_loc))
        self.credit.clickBtn("确定按钮",*(self.credit.creditBtn_loc))


    @unittest.skipIf(scripts.getRunFlag('CREDIT', 'testCase1') == 'N', '验证执行配置')
    @ddt.data(*creditData)
    def testCase1(self,data):
        '''积分换礼'''
        print '{0}'.format(data['desc'])
        self.creditFunc(data) #输入手机号,或卡号,进入积分换礼页面
        self.credit.iterClick("积分规则",*(self.credit.credit_checkbox_loc))
        self.credit.inputText(data['ExchangeNumber'],'积分数量',*(self.credit.creditNum_loc))
        self.credit.inputText(data['ExchangeDetail'],'积分详情',*(self.credit.detail_loc))
        self.credit.clickBtn("确定按钮",*(self.credit.sendMessageBtn_loc))
        #print self.driver.find_element_by_xpath('/html/body/div[5]').is_displayed()
        self.credit.assertPaySuccess #成功兑换断言

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()




if __name__=="__main__":
    suite = unittest.TestSuite()
    tests = [unittest.TestLoader().loadTestsFromTestCase(TestCreditPage)]
    suite.addTests(tests)
    filePath = os.path.join(gl.reportPath, 'Report.html')  # 确定生成报告的路径
    print filePath

    with file(filePath, 'wb') as fp:
        runner = HTMLTESTRunnerCN.HTMLTestRunner(
            stream=fp,
            title=u'UI自动化测试报告',
            description=u'详细测试用例结果',  # 不传默认为空
            tester=u"yhleng"  # 测试人员名字，不传默认为小强
        )
        # 运行测试用例
        runner.run(suite)
        fp.close()
