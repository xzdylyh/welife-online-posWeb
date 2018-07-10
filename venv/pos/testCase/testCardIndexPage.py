#coding=utf-8
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pos.pages import cardIndexPage
import unittest,ddt,os,time
from pos.lib import scripts
from pos.lib.excel import Excel
from pos.lib import gl,HTMLTESTRunnerCN

cardShopData = [{"desc": u"实体储值卡售卖", "pagetitle": u"储值卡售卖 - 微生活POS系统","assert":u"该张储值卡已经售卖"}]


@ddt.ddt
class TestCardIndexPage(unittest.TestCase):
    """储值售卖模块"""
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.url = 'http://pos.beta.acewill.net/card/index'
        cls.excel = Excel(os.path.join(gl.dataPath, 'posChargeCard.xls').decode('utf-8'))


    @unittest.skipIf(scripts.getRunFlag('CARDINDEX', 'testCase1') == 'N', '验证执行配置')
    @ddt.data(*cardShopData)
    def testCase1(self,data):
        """储值卡售卖-实体储值卡"""
        print '功能:{0}'.format(data['desc'])

        """前置初始操作"""
        self.card = cardIndexPage.CardIndexPage(self.url,self.driver,data['pagetitle'])
        self.card.open #打开目标地址

        cardNo = float(self.excel.getCardNo(cell_col=0,cell_valueType=1)).__int__().__str__()
        """储值售卖页面"""
        #self.card.selectDownList(option=0,index=0) #按索引,选择第一个.索引从0开始

        self.card.clickBtn('储值卡类型',*(self.card.card_Type_loc))
        self.card.inputText(cardNo,'储值卡号',*(self.card.card_Numer_loc))
        self.card.clickBtn('确定',*(self.card.card_ConfirmBtn_loc))
        self.card.clickBtn('再次确定',*(self.card.card_toConfirmBtn_loc))

        """后置断言操作"""
        self.card.clickBtn('储值卡类型',*(self.card.card_Type_loc))
        self.card.inputText(cardNo,'储值卡号',*(self.card.card_Numer_loc))
        self.assertEqual(self.card.assertChareSuccess,data['assert'],msg='断言已售的卡不能再售,来判断售卡成功')


    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()




if __name__=="__main__":
    scripts.rmDirsAndFiles(gl.imgPath)
    suite = unittest.TestSuite()

    tests = [unittest.TestLoader().loadTestsFromTestCase(TestCardIndexPage)]
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