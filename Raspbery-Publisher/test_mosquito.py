import random
import time

from paho.mqtt import client as mqtt_client

broker = 'test.mosquitto.org'
port = 1883
topic = "ariel"
client_id = f'python-mqtt-{random.randint(0, 1000)}'
# username = 'emqx'
# password = 'public'
lista = "solar,precipitation,strikes,strikeDistance,windSpeed,windDirection,gustWindSpeed,airTemperature"
# otra_lista = [12,15,18,21,45,83,98,78]

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
    # Set Connecting Client ID
    client = mqtt_client.Client(client_id)
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client
"""
def armar_diccionario_con_lista(lista, otra_lista):
    dict_from_list = dict(zip(lista, otra_lista))
    return dict_from_list
"""

def publish(client):
    msg_count = 0
    while True:
        time.sleep(1)
        # msg = armar_diccionario_con_lista(lista, otra_lista)
        msg = lista
        result = client.publish(topic, msg)
        result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
        msg_count += 1
"""
def new_publish():
    # msg = armar_diccionario_con_lista(lista, otra_lista)
    msg = lista
    publish.multiple(msg, broker)
"""
def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)
    # new_publish()
    # msgs = tuple(lista)
    # publish.multiple(msgs, broker)

if __name__ == '__main__':
    run()
