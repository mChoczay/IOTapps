from flask import Flask, request, render_template
from flask_restful import Api, Resource
import requests
import json
import paho.mqtt.client as mqtt
import time
from configing import readconf



app = Flask(__name__)



broker = "test.mosquitto.org"
client = mqtt.Client()
client.connect(broker)
client.loop_start()
client.subscribe("temat")

def on_message(client, userdata, message):
    config_file = f"{serwer}.ini"
    m_decode = str(message.payload.decode("utf-8"))
    
    
    if readconf(config_file,"aktuator") == 'True':
        signal = {"signal" : 1}
        new_data = int(m_decode)
        new_data -= int(readconf(config_file,"active"))
        with open(f"data{serwer}.txt", "a") as file:
            file.write(new_data)
            file.write("\n")
        requests.post("http://127.0.0.1:5000/odbieranie",signal)
        client.publish("temat1",payload=new_data)
        
    elif int(m_decode) > int(readconf(config_file,"breakpoint")):
        signal = {"signal" : 1}
        new_data = int(m_decode)
        new_data -= int(readconf(config_file,"active"))
        
        message_signal = readconf(config_file,"message")
        message_dict = {"message":message_signal}

        
        with open(f"data{serwer}.txt", "a") as file:
            file.write(str(new_data))
            file.write("\n")



        requests.post("http://127.0.0.1:5000/updater/sygnal",message_dict)
        requests.post("http://127.0.0.1:5000/odbieranie",signal)
        
        client.publish("temat1",payload=new_data)


    else:
        signal = {"signal" : 1}
        requests.post("http://127.0.0.1:5000/odbieranie",signal)
        client.publish("temat1",payload=m_decode)
        
    print(f"Received message:{m_decode}")
    return m_decode

@app.route('/',methods=['GET', 'POST'])
def main():
    data = request.form.to_dict()
    data = data["data"]
    config_file = f"{serwer}.ini"
    new_data = int(data)
    if readconf(config_file,"aktuator") == 'True': 
        new_data -= int(readconf(config_file,"active"))
        data = str(new_data)
        with open(f"data{serwer}.txt", "a") as file:
            file.write(data)
            file.write("\n")

        data = {"data" : data}
        requests.post("http://127.0.0.1:5000/odbieranie",params = data)

    elif int(new_data) > int(readconf(config_file,"breakpoint")):
        new_data -= int(readconf(config_file,"active"))
        data = str(new_data)
        with open(f"data{serwer}.txt", "a") as file:
            file.write(data)
            file.write("\n")
        data = {"data" : data}

        message_signal = readconf(config_file,"message")
        message_dict = {"message":message_signal}

        requests.post("http://127.0.0.1:5000/updater/sygnal",message_dict)
        requests.post("http://127.0.0.1:5000/odbieranie",params = data)
        
    else:
        data = {"data" : data}
        requests.post("http://127.0.0.1:5000/odbieranie",params = data)

    if readconf(config_file,"metoda") == 'MQTT':
        client.on_message = on_message

    return render_template("agregator.html")

@app.route('/serwer', methods = ['GET','POST'])
def serwer():
    data = request.args.to_dict()
    global serwer
    serwer = data["serwer"]
    print(serwer)
    return render_template("agregator.html")


app.run(debug=True, port=5060)
client.loop_stop()
