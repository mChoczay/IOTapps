from configparser import ConfigParser


CONFIG_OBJECT = ConfigParser()

CONFIG_OBJECT["USERINFO"] = {
   "1" : "0",
   "2" : "0",
   "3" : "0"
}

def createServerConfig(a, config_object = CONFIG_OBJECT):
    with open(f'{a}.ini', 'w') as conf:
        config_object.write(conf)

