#_*_coding:utf-8_*_
import time,os,zipfile
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
        cont = fp.read()
        fp.close()

    ret = yaml.load(cont)
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

def CookInfo(func):
    """
    从配置文件获取cookies信息
    :param func: 函数名
    :return: 函数
    """
    def warpper(*args,**kwargs):
        yamldict = getYamlfield(os.path.join(gl.configPath, 'config.yaml'))
        cook1= yamldict['CONFIG']['Cookies']['LoginCookies']
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
        yamldict = getYamlfield(os.path.join(gl.configPath, 'config.yaml'))
        sleepTime = float(yamldict['RUNING']['REPLAY']['Time']) / 1000
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
            config = getYamlfield(gl.configFile)
            ret = None
            if config['HightLight'] ==1:
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





if __name__=="__main__":
    #print json.dumps(getRunFlag('testCouponSendAndCancel')).decode('unicode-escape')
    demo(cook='')

