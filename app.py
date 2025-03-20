from flask import Flask, render_template
import random
from paho.mqtt import client as mqtt_client
import json
from turbo_flask import Turbo
import threading
import time
import sys

app = Flask(__name__)
broker = 'mqtt.test4iot.de' 
port = 8183
# Message's directory on mqtt explorer.
topic = "Oi4/OTConnector/hilscher.com/netFIELD,20App,20OPC,20UA,20IO-Link,20Adapter/1917.011/netfield-app-opc-ua-io-link-adapter/Pub/Data" 
# Generate a Client ID with the subscribe prefix.
client_id = f'subscribe-{random.randint(0, 100)}'
username = 'iotuser'
password = '!Router_20'
turbo = Turbo(app)


def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        message = json.loads(msg.payload.decode())["Messages"]

        global s1, temp_ob1, out1_ob1, out2_ob1, temp_pro1, out1_pro1, out2_pro1
        s1 = message[0]["Source"]
        temp_ob1 = message[0]["Payload"]["Temperature"]
        out1_ob1 = message[0]["Payload"]["OUT1"]
        out2_ob1 = message[0]["Payload"]["OUT2"]
        temp_pro1 = message[1]["Payload"]["Temperature"]
        out1_pro1 = message[1]["Payload"]["OUT1"]
        out2_pro1 = message[1]["Payload"]["OUT2"]

        global s2, crest_ob2, stat_ob2, out1_ob2, out2_ob2, temp_ob2, apeak_ob2, arms_ob2, vrms_ob2
        global crest_pro2, stat_pro2, out1_pro2, out2_pro2, temp_pro2, apeak_pro2, arms_pro2, vrms_pro2
        s2 = message[2]["Source"]
        crest_ob2 = message[2]["Payload"]["Crest"]
        stat_ob2 = message[2]["Payload"]["Device status"]
        out1_ob2 = message[2]["Payload"]["OUT1"]
        out2_ob2 = message[2]["Payload"]["OUT2"]
        temp_ob2 = message[2]["Payload"]["Temperature"]
        apeak_ob2 = message[2]["Payload"]["a-Peak"]
        arms_ob2 = message[2]["Payload"]["a-Rms"]
        vrms_ob2 = message[2]["Payload"]["v-Rms"]
        crest_pro2 = message[3]["Payload"]["Crest"]
        stat_pro2 = message[3]["Payload"]["Device status"]
        out1_pro2 = message[3]["Payload"]["OUT1"]
        out2_pro2 = message[3]["Payload"]["OUT2"]
        temp_pro2 = message[3]["Payload"]["Temperature"]
        apeak_pro2 = message[3]["Payload"]["a-Peak"]
        arms_pro2 = message[3]["Payload"]["a-Rms"]
        vrms_pro2 = message[3]["Payload"]["v-Rms"]

    client.subscribe(topic)
    client.on_message = on_message


@app.route("/")
def hello():
    return render_template("index.html")


@app.context_processor
def inject_load():
    return {
        "s1": s1, "temp_ob1": temp_ob1, "out1_ob1": out1_ob1, "out2_ob1": out2_ob1, "temp_pro1": temp_pro1, "out1_pro1": out1_pro1, "out2_pro1": out2_pro1,
        "s2": s2, "crest_ob2": crest_ob2, "stat_ob2": stat_ob2, "ou1_ob2": out1_ob2, "out2_ob2": out2_ob2, "temp_ob2": temp_ob2, "apeak_ob2": apeak_ob2, "arms_ob2": arms_ob2, "vrms_ob2": vrms_ob2,
        "crest_pro2": crest_pro2, "stat_pro2": stat_pro2, "ou1_pro2": out1_pro2, "out2_pro2": out2_pro2, "temp_pro2": temp_pro2, "apeak_pro2": apeak_pro2, "arms_pro2": arms_pro2, "vrms_pro2": vrms_pro2
            }


def update_load():
    with app.app_context():
        while True:
            time.sleep(5)
            turbo.push(turbo.replace(render_template('index.html'), 'load'))


with app.app_context():
    threading.Thread(target=update_load).start()


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_start()
    # Flask runs in parallel with Broker connection.
    app.run(host='0.0.0.0', port=5000) 
    client.loop_end()


if __name__ == '__main__':
    run()






        
