#coding=utf-8
from selenium import webdriver
from pos.pages import numbercardPage
import unittest,ddt,os
from pos.lib.excel import Excel
from pos.lib import scripts
from pos.lib import gl,HTMLTESTRunnerCN
import time,json


numberCardData = [{"useNum":1,"phoneOrCard":"13712345678","desc":u"次卡消费,正常流程","title":u"次卡消费 - 微生活POS系统"}]

@ddt.ddt
class TestNumberCardPage(unittest.TestCase):
    """次卡消费模块"""
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.url = 'http://pos.beta.acewill.net/numbercard'

    @unittest.skipIf(scripts.getRunFlag('NUMBERCARD', 'testCase1') == 'N', '验证执行配置')
    @ddt.data(*numberCardData)
    def testCase1(self,data):
        """次卡消费"""
        print '功能:{0}'.format(data['desc'])

        self.number = numbercardPage.NumberCardPage(self.url,self.driver,data['title'])
        self.number.open #打开目标地址

        """输入手机号或卡号进入次卡消费界面"""
        self.number.inputText(data['phoneOrCard'],'手机号',*(self.number.number_phone_Loc))
        self.number.clickBtn('确定',*(self.number.number_conrimBtn_loc))

        """次卡消费界面,操作"""
        self.number.inputText(data['useNum'],'次数',*(self.number.number_usenum_loc))
        self.number.clickBtn('确定',*(self.number.number_submit_loc))

        """检查断言"""
        self.assertTrue(self.number.assertSuccess,msg='检查消费后,返回到,输入手机号界面')


    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()



if __name__=="__main__":
    suite = unittest.TestSuite()

    tests = [unittest.TestLoader().loadTestsFromTestCase(TestNumberCardPage)]
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