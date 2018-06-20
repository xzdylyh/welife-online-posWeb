#coding=utf-8
from selenium import webdriver
from pos.pages import bjPrintPage
import unittest,ddt,os
from pos.lib import scripts
from pos.lib import gl,HTMLTESTRunnerCN
import time

printData = [{"startDate": gl.curDate, "endDate": gl.curDate,"desc":u"班结小票打印正常流程"}]

@ddt.ddt
class TestBjPrintPage(unittest.TestCase):
    """班结小票打印"""
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.url = 'http://pos.beta.acewill.net/consume/list'

    @unittest.skipIf(scripts.getRunFlag('PRINT', 'testCase1') == 'N', '验证执行配置')
    @ddt.data(*printData)
    def testCase1(self,data):
        """班结小结打印"""
        print '功能:{0}'.format(data['desc'])
        self.bjPrint = bjPrintPage.BjPrintPage(self.url,self.driver,u'消费 - 微生活POS系统')
        self.bjPrint.open #打开交易流水
        self.bjPrint.clickBtn('打印班结小票',*(self.bjPrint.bjPrintLink_loc))
        """
        self.bjPrint.inputText(data['startDate'],'开始时间',*(self.bjPrint.bjPrintStartDate_loc))
        self.bjPrint.inputText(data['endDate'],'结束时间',*(self.bjPrint.bjPrintEndDate_loc))
        """
        self.bjPrint.clickBtn('打印',*(self.bjPrint.bjPrintBtn_loc))
        time.sleep(5) #等待3秒
        self.bjPrint.switch_window #切换到新窗口
        #self.bjPrint.clickBtn('pop打印',*(self.bjPrint.bjPrintPopBtn_loc))
        """断言"""
        self.assertTrue(self.bjPrint.assertPrint,msg='点击打印后,打印页面消失,弹出打印机')#断言弹出最后打印界面,打印按钮存在


    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


if __name__=="__main__":
    suite = unittest.TestSuite()

    tests = [unittest.TestLoader().loadTestsFromTestCase(TestBjPrintPage)]
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
