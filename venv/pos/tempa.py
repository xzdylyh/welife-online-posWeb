#coding=utf-8
from pos.lib import gl
from pos.lib import scripts
import os
a = u'22976.00元'
print a[:-1]

def Config(func):
    def war(*args,**kwargs):
        configData = scripts.getYamlfield(os.path.join(gl.configPath,'config.yaml'))
        return func(configData,**kwargs)
    return war()

@Config
def kkkk(config):
    print config['CONFIG']['Cookies']['LoginCookies']