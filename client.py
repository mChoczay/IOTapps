from flask import Flask, request, render_template
from flask_restful import Api, Resource
import requests
import paho.mqtt.client as mqtt
from newconfig import createConfig
from newserwerconfig import createServerConfig
from configing import updateconf, readconf
from counter import counter

serwer_file = "serwers.ini"


app = Flask(__name__)

broker = "test.mosquitto.org"
client = mqtt.Client()
client.connect(broker)
client.loop_start()
client.subscribe("temat1")

def on_message(client, userdata, message):
    m_decode = str(message.payload.decode("utf-8"))
    print(f"Received message:{m_decode}")
    return m_decode

def filetolist(file):
    filelist = []
    for i in file:
        filelist.append(i)
    return filelist

@app.route('/')
def main():
    try:
        with open('serwers.ini') as f:
            f.readlines()
    except IOError:
        createServerConfig('serwers') 
    return render_template("main.html")

@app.route('/odbieranie',methods=['GET', 'POST'])
def odbieranie():
    if readconf(f'{current_serwer}.ini',"metoda") == "HTTP":
        client_data = request.args.to_dict()
        print(client_data['data'])
    elif readconf(f'{current_serwer}.ini',"metoda") == "MQTT":
        client.on_message = on_message
    return render_template("index.html")

@app.route('/panel',methods=["GET","POST"])
def panel():
    name = request.form.to_dict()
    createConfig(name['rejestracja'])

    server_number = str(counter())
    new_serwer = name['rejestracja']
    updateconf(serwer_file,server_number,new_serwer)

    global current_serwer
    current_serwer = new_serwer

    print(current_serwer)

    return render_template("index.html")

@app.route("/method",methods=["GET","POST"])
def wybor():
    if request.method == "GET":
        return render_template("index.html")
    else:
        data = request.form.to_dict()
        requests.post(f"http://127.0.0.1:{current_serwer}/wybor_metody",params = data)
        return render_template("index.html")

@app.route("/frequency",methods=["GET","POST"])
def zakres():
    if request.method == "GET":
        return render_template("index.html")
    else:
        data = request.form.to_dict()
        requests.post(f"http://127.0.0.1:{current_serwer}/czestotliwosc",params = data)
        return render_template("index.html") 

@app.route("/switch",methods=["GET","POST"])
def wlacznik():
    if request.method == "GET":
        data = request.form.to_dict()
        return render_template("index.html")
    else:
        data = request.form.to_dict()
        requests.post(f"http://127.0.0.1:{current_serwer}/wlacznik",params = data)
        return render_template("index.html")
        
@app.route("/sourcestatus",methods=["GET","POST"])
def status():
    status = readconf(f'{current_serwer}.ini',"wlacznik")
    return render_template("index.html", value2 = status, value3 = current_serwer)

@app.route('/updater/sygnal',methods=['GET', 'POST'])
def syngal():
    client_data = request.form.to_dict()
    print(client_data['message'])
    return render_template("index.html")

@app.route("/updater",methods=["GET","POST"])
def aktuator():
    if request.method == "GET":
        return render_template("index.html")
    else:
        data = request.form.to_dict()
        requests.post(f"http://127.0.0.1:{current_serwer}/aktuator",params = data)
        return render_template("index.html")


@app.route('/serwer',methods=["GET","POST"])
def serwer():
    number = request.form.to_dict()['serwer']
    server_adress = readconf(serwer_file,number)

    global current_serwer
    current_serwer = server_adress
    data = {"serwer" : current_serwer}
    requests.post("http://127.0.0.1:5060/serwer", params = data)

    print(current_serwer)
    
    return render_template("index.html",value = number)

@app.route('/wyswietlanie',methods=["GET","POST"])
def wyswietlanie():

    n = int(request.form.to_dict()['wyswietlanie'])
    file = open("data5050.txt","r")
    for i in file:
        print(i)
        n-=1
        if n <=0:
            break
    return render_template("index.html")

app.run(debug=True)
client.loop_stop()