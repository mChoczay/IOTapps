from configparser import ConfigParser


CONFIG_OBJECT = ConfigParser()

CONFIG_OBJECT["USERINFO"] = {
    "metoda" : "None",
    "wlacznik" : "True",
    "czestotliwosc" : "0",
    "aktuator" : "False",
    "message": "0",
    "active" : "0",
    "breakpoint" : "0"
}

def createConfig(a, config_object = CONFIG_OBJECT):
    with open(f'{a}.ini', 'w') as conf:
        config_object.write(conf)

