#_*_coding:utf-8_*_
import time,os
import yaml,json
from pos.lib import gl



"""写YAML文件内容"""
def writeYmal(yamlPath,data):
    """
    写YAML文件内容
    :param yamlPath: YAML文件路径
    :param data: 写入的数据
    :return: 无
    """
    fp = open(yamlPath,'w')
    yaml.dump(data,fp)
    fp.close()


"""读取YAML文件内容"""
def getYamlfield(yamlpath):
    """
    读取YAML内容
    :param yamlpath: xxxx.YAML文件所在路径
    :return: 指定节点内容
    """
    f = open(yamlpath,'r')
    cont = f.read()
    ret = yaml.load(cont)
    f.close()
    return ret


"""获取执行标记"""
def getRunFlag(scenarioKey,casename):
    """
    获取运行标记，来决定是否执行
    :param scenarioKey:
    :return: Y 或 N
    """
    yamldict = getYamlfield(os.path.join(gl.configPath,'config.yaml'))
    return yamldict['RUNING'][scenarioKey]['Flag'][casename]['Flag']


def Replay(func):
    """
    执行函数之后,等封若干毫秒
    :param func: 函数名
    :return: wrapper
    """
    def wrapper(*args,**kwargs):
        func(*args,**kwargs)
        yamldict = getYamlfield(os.path.join(gl.configPath, 'config.yaml'))
        time.sleep(yamldict['RUNING']['REPLAY']['Time'] / 1000)
        return func
    return wrapper


"""获取配置数据，装饰器"""
def Config(func):
    """
    配置信息，装饰器
    :param func: 函数
    :return: config.yaml字典内容
    """
    def wrapper(*args,**kwargs):
        configData = getYamlfield(os.path.join(gl.configPath,'config.yaml'))
        return func(configData,**kwargs)
    return wrapper

@Replay
def demo():
    print 'this is demo.'

if __name__=="__main__":
    #print json.dumps(getRunFlag('testCouponSendAndCancel')).decode('unicode-escape')
    demo()

