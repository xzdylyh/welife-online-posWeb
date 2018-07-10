#coding=utf-8
from selenium import webdriver
from pos.pages import consumeListPage
import unittest,ddt,os
from pos.lib.excel import Excel
from pos.lib import scripts
from pos.lib import gl,HTMLTESTRunnerCN
import time,json

consumeData = [{"consumeListTitle": "消费流水 - 微生活POS系统","desc":u"撤销消费正常流程"}]


@ddt.ddt
class TestConsumeListPage(unittest.TestCase):
    """交易流水-消费"""
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.url = 'http://pos.beta.acewill.net/consume/list'


    @unittest.skipIf(scripts.getRunFlag('CONSUMELIST', 'testCase1') == 'N', '验证执行配置')
    @ddt.data(*consumeData)
    def testCase1(self,data):
        """交易流水-撤销消费"""
        print '功能:{0}'.format(data['desc'])
        self.consumeList = consumeListPage.ConsumeListPage(self.url,self.driver,data['consumeListTitle'])
        self.consumeList.open #打开目标地址

        self.consumeList.clickBtn('撤销消费',*(self.consumeList.undo_deal_loc))
        self.consumeList.clickBtn('确定',*(self.consumeList.undo_dealBtn_loc))
        """断言"""
        self.assertTrue(self.consumeList.assertCancelSuccess) #断言,弹出撤销成功div框
        txt = self.consumeList.find_element(*(self.consumeList.undo_assert_list_loc)).text #断言弹出成功提示div
        self.assertEqual(txt,u'撤销消费',msg='撤销消费,列表中增加一条撤销记录')





    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()





if __name__=="__main__":
    suite = unittest.TestSuite()

    tests = [unittest.TestLoader().loadTestsFromTestCase(TestConsumeListPage)]
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
