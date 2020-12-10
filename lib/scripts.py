import time, os, random, zipfile
import yaml, json
from selenium import webdriver
from lib import gl
from lib.config import CONF


def rnd_num(sat_num=1000,end_num=4000):
    """
    生成随机数。
    :param num:
    :return:
    """
    ret = random.randint(sat_num,end_num)
    return ret

def select_Browser_WebDriver():
    """
    根据config.yaml配置文件，来选择启动的浏览器
    :return:
    """
    #读取config.yam配置文件中，浏览器配置
    broName = CONF.read()['CONFIG']['Browser']

    #根据borName决定，启动，哪个浏览器
    if str(broName).strip().lower() == 'chrome':
        driver = webdriver.Chrome()
    elif str(broName).strip().lower() == 'firefox':
        driver = webdriver.Firefox()
    else:
        driver = webdriver.Ie()
    return driver


"""写YAML文件内容"""
def writeYmal(yamlPath,data):
    """
    写YAML文件内容
    :param yamlPath: YAML文件路径
    :param data: 写入的数据
    :return: 无
    """
    with open(yamlPath,'wb') as fp:
        yaml.dump(data, fp)
        fp.close()

"""读取YAML文件内容"""
def getYamlfield(yamlpath):
    """
    读取YAML内容
    :param yamlpath: xxxx.YAML文件所在路径
    :return: 指定节点内容
    """
    with open(yamlpath,'rb') as fp:
        cont = fp.read().decode('utf-8')
        fp.close()

    ret = yaml.load(cont)
    return ret



def getBaseUrl(key):
    """
    根据指定的key获取config中配置的url
    :param key: config中key值
    :return: url
    """
    return CONF.read()['BASE_URL'][key]



"""获取执行标记"""
def getRunFlag(scenarioKey,casename):
    """
    获取运行标记，来决定是否执行
    :param scenarioKey:
    :return: Y 或 N
    """
    return CONF.read()['RUNING'][scenarioKey]['Flag'][casename]['Flag']

def CookInfo(func):
    """
    从配置文件获取cookies信息
    :param func: 函数名
    :return: 函数
    """
    def warpper(*args,**kwargs):
        cook1= CONF['CONFIG']['Cookies']['LoginCookies']
        return func(cook=cook1,*args,**kwargs)
    return warpper


def Replay(func):
    """
    回放速度
    :param func: 函数名
    :return: wrapper
    """
    def wrapper(*args,**kwargs):
        func(*args,**kwargs)
        sleepTime = float(CONF.read()['RUNING']['REPLAY']['Time']) / 1000
        time.sleep(sleepTime)
        return func
    return wrapper


"""元素高亮显示配置，装饰器"""
def hightlightConfig(key):
    """
    配置元素，是否高亮显示
    :param key: config.yaml 中关键字 HightLight:1 高亮 其它忽略
    :return:
    """
    def _wrapper(func):
        def wrapper(*args,**kwargs):
            ret = None
            if CONF.read()['HightLight'] ==1:
                ret = func(*args,**kwargs)
            return ret
        return wrapper
    return _wrapper



def rmDirsAndFiles(dirpath):
    """
    删除目标,目录下文件及文件夹
    :param dirpath: 目标目录
    :return: 无
    """
    listdir = os.listdir(dirpath)
    if listdir:
        for f in listdir:
            filepath = os.path.join(dirpath,f)
            if os.path.isfile(filepath):
                os.remove(filepath)
            if os.path.isdir(filepath):
                os.rmdir(filepath)


def zipDir(dirpath,outFullName):
    """
    压缩指定文件夹
    :param dirpath: 目标文件夹路径
    :param outFullName: 压缩文件保存路径+xxxx.zip
    :return: 无
    """
    zip = zipfile.ZipFile(outFullName,"w",zipfile.ZIP_DEFLATED)
    for path,dirnames,filenames in os.walk(dirpath):
        # 去掉目标跟路径，只对目标文件夹下边的文件及文件夹进行压缩
        fpath = path.replace(dirpath,'')

        for filename in filenames:
            zip.write(os.path.join(path,filename),os.path.join(fpath,filename))
    zip.close()


def replayCaseFail(num=3):
    """
    测试case失败后，重新执行功能
    :param num: 失败最多可以执行次数，默认为3次
    :return: fun本身或者抛出异常
    """
    def _warpper(func):
        def warpper(*args,**kwargs):
            raise_info = None
            rnum = 0
            for i in range(num):
                rnum +=1
                try:
                    ret = func(*args,**kwargs)
                    if rnum > 1:
                        print('重试{}次成功'.format(rnum))
                    return ret
                except Exception as ex:
                    raise_info = ex
            print('重试{}次,全部失败'.format(rnum))
            raise raise_info
        return warpper
    return _warpper


def send_dding_msg(token, msg):
    '''
    推送消息到钉群
    '''
    import requests
    payload = {
        "msgtype": "text",
        "text": {
            "content": msg,
            # "mentioned_mobile_list":["13718651998"],
        }
    }
    headers = {
        'Content-Type': 'application/json'
    }
    d_url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={}'.format(token)

    res = requests.request('POST', d_url, headers=headers, json=payload)

    return res



if __name__=="__main__":
    token = '2c412f54-b815-45c5-b928-8fec114d1ea9'
    send_dding_msg(token, '测试消息')
