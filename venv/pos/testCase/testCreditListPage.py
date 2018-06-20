# coding=utf-8
from selenium import webdriver
from pos.pages import creditListPage
import unittest, ddt, os
from pos.lib.excel import Excel
from pos.lib import scripts
from pos.lib import gl, HTMLTESTRunnerCN
import time, json

creditData = [{"CreditListTitle":u"积分换礼流水 - 微生活POS系统","desc": u"积分换礼-撤销积分"}]


@ddt.ddt
class TestCreditListPage(unittest.TestCase):
    """交易流水模块-积分换礼"""

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.url = 'http://pos.beta.acewill.net/credit/list'

    @unittest.skipIf(scripts.getRunFlag('CREDITLIST', 'testCase1') == 'N', '验证执行配置')
    @ddt.data(*creditData)
    def testCase1(self, data):
        """交易流水-撤销积分"""
        print '功能:{0}'.format(data['desc'])
        self.creditList = creditListPage.CreditListPage(self.url,self.driver,data['CreditListTitle'])
        self.creditList.open #打开目标地址
        """撤销积分"""
        self.creditList.clickBtn('撤销积分',*(self.creditList.undo_LinkBtn_loc))
        self.creditList.clickBtn('确定',*(self.creditList.undo_Btn_loc))
        """断言"""
        txt=self.creditList.assertCancelSuccess
        self.assertEqual(txt,'撤销积分换礼',msg='撤销积分后,再列表显示一条,状态为撤销积分换礼')


    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


if __name__ == "__main__":
    suite = unittest.TestSuite()

    tests = [unittest.TestLoader().loadTestsFromTestCase(TestCreditListPage)]
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
