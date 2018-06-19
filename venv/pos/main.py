#_*_coding:utf-8_*_
import unittest
import os,time,json
from pos.lib import (HTMLTESTRunnerCN,gl)
from pos.testCase.testConsumePage import TestConsumePage
from pos.testCase.testChargePage import TestChargePage
from pos.testCase.testCreditPage import TestCreditPage


if __name__=="__main__":
    suite = unittest.TestSuite()
    tests = [unittest.TestLoader().loadTestsFromTestCase(TestConsumePage),
             unittest.TestLoader().loadTestsFromTestCase(TestChargePage),
             unittest.TestLoader().loadTestsFromTestCase(TestCreditPage)]

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

