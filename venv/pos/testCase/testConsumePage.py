#coding=utf-8
from selenium import webdriver
from pos.pages import consumePage
import unittest,ddt,os
from pos.lib import gl,HTMLTESTRunnerCN

testData = [{"phoneOrCard":"13522656892","desc":'''手机号'''},
            {"phoneOrCard":"1726002880387638","desc":"卡号"}]

@ddt.ddt
class TestConsumePage(unittest.TestCase):
    '''消费模块'''
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Firefox()
        cls.url = 'https://pos.acewill.net/consume'
        #cookies 免登录，有效期一天。
        cls.cookinfo = {"pos_entry_number":"13522656892",
               "pos_entry_actualcard":"1726002880387638",
               "pos_bid":"2760627865",
               "pos_mid":"1134312064",
               "pos_sid":"3704059614",
               "pos_sign":"2a6ce62800f47551fd2826dab449b6cb"}

    @ddt.data(*testData)
    def testCase1(self,data):
        u'''根据手机号或卡号查询消费'''
        print "根据{0}查询消费".format(data['desc'])
        consume = consumePage.ConsumePage(self.url,self.driver,'消费 - 微生活POS系统')

        # 打开浏览器，并转到消费页
        consume.open(ck_dict=self.cookinfo)
        # 选择会员卡号/手机号
        consume.selectTab(*(consume.selectCardNo_loc))
        #输入卡号或手机号
        consume.inputText(data['phoneOrCard'],*(consume.inputCardorPhone_loc))
        #点击确定按钮
        consume.clickBtn(*(consume.confirmBtn_loc))

        #断言
        self.assertTrue(consume.assertCustom,msg='消费->确定->未找到手机号')


    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

if __name__=="__main__":
    suite = unittest.TestSuite()

    tests = [unittest.TestLoader().loadTestsFromTestCase(TestConsumePage)]
    # tests = [unittest.TestLoader().loadTestsFromTestCase(ScenarioTest)]
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
