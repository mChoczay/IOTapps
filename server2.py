from flask import Flask, request
import paho.mqtt.client as mqtt
import time
import json
import requests
import time
from data_menager import read_csv
from configing import updateconf, readconf

app = Flask(__name__)
SOURCE = 'wave_height.csv'

broker = "test.mosquitto.org"
client = mqtt.Client()
client.connect(broker)


data_list = read_csv(SOURCE)
config_file = "5051.ini"

config_keys = {
    "switch": "wlacznik",
    "updater": "aktuator",
    "frequency": "czestotliwosc",
    "method": "metoda",
}

@app.route('/wybor_metody',methods=['POST'])
def wybor_metody():

    client_data = request.args.to_dict()
    if "metoda" in client_data:
        global metoda
        metoda = client_data["metoda"]
        validation = [
            "HTTP" == metoda, 
            "MQTT" == metoda 
        ]
        if any(validation):
            topic = "metoda"
            updateconf(config_file, topic, client_data['metoda'])
            return client_data
        else:
            return{
                "status": 400,
                "message": "Wybrana metoda nie jest obslugiwana"
            }, 400
    else:
        return {
            "status": 400,
            "message": "Zle argumenty"
        }, 400  


@app.route('/czestotliwosc',methods=['POST'])
def czestotliwosc():
    topic = "czestotliwosc"
    client_data = request.args.to_dict()
    updateconf(config_file, topic, client_data['czestotliwosc']) 
    return client_data

@app.route('/wlacznik',methods=['GET','POST'])
def wlacznik():
    updateconf(config_file, "message", "Fale sa zbyt wysokie, zmniejszam wartosc generatora")
    updateconf(config_file, "active", "100")
    updateconf(config_file, "breakpoint", "300")

    client_data = request.args.to_dict()
    if "wlacz" in client_data:
        global wlacz
        wlacz = client_data["wlacz"]
        validation = [
            "True" == wlacz, 
            "False" == wlacz 
        ]

        if any(validation):
            topic = config_keys["switch"]
            topic2 = config_keys["frequency"]
            updateconf(config_file, topic, client_data['wlacz'])
            status = readconf(config_file,topic)

            if status == 'True':
                for data in data_list:
                    status = readconf(config_file,topic)
                    freq = readconf(config_file,topic2)
                    if status == 'True':
                        metoda = readconf(config_file,config_keys["method"])
                        if metoda == "HTTP":
                            print("wysylam http")
                            
                            data = {"data" : data}
                            requests.post("http://127.0.0.1:5060/",data = data)
                        else:
                            print("wysylam mqtt")
                            data = int(data)
                            triger = {"data" : 1}
                            requests.post("http://127.0.0.1:5060/",data = triger)
                            client.publish("temat", payload= data)
                    else:
                        return {"1":1}
                    time.sleep(int(freq))
            else:
                return {"1":1}
        else:
            return{
                "status": 400,
                "message": "Wybrana opcja nie jest obslugiwana"
            }, 400
    else:
        return {
            "status": 400,
            "message": "Zle argumenty"
        }, 400  

@app.route('/aktuator',methods=['POST'])
def aktuator():
    client_data = request.args.to_dict()
    if "aktuator" in client_data:
        global aktuator
        aktuator = client_data["aktuator"]
        validation = [
            "True" == aktuator, 
            "False" == aktuator 
        ]
        if any(validation):
            topic = "aktuator"
            updateconf(config_file, topic, client_data['aktuator'])
            return client_data
        else:
            return{
                "status": 400,
                "message": "Wybrana opcja nie jest obslugiwana"
            }, 400
    else:
        return {
            "status": 400,
            "message": "Zle argumenty"
        }, 400  

app.run(port=5051,debug=True)