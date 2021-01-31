from configparser import ConfigParser


CONFIG_OBJECT = ConfigParser()

def readconf(file,topic,config_object = CONFIG_OBJECT):
    config_object.read(file)
    userinfo = config_object["USERINFO"][topic]
    return userinfo

def updateconf(file, topic, data, config_object = CONFIG_OBJECT):
    config_object.read(file)
    config_object["USERINFO"][topic] = data
    with open(file, 'w') as conf:
        config_object.write(conf)
