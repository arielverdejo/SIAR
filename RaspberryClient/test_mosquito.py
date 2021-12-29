#! /usr/bin/env python3

import serial
import socket

import random
import time

from paho.mqtt import client as mqtt_client

#Variables

#host = "192.168.0.101"
#port = 8050

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

def publish(client, cadena):
    msg_count = 0
    #while True:
    time.sleep(1)
    # msg = armar_diccionario_con_lista(lista, otra_lista)
    msg = cadena
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
"""
def enviar_datos(mensaje):
    #Creación de un objeto socket (lado cliente)
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #Conexión con el servidor. Parametros: IP (puede ser del tipo 192.1$
    clientSocket.connect((host, port))
    print("Conectado al servidor")
    #Creamos un bucle para retener la conexion
    #Instanciamos una entrada de datos para que el cliente pueda enviar$
    #mens = raw_input("Mensaje desde Cliente a Servidor >> ")
    #for dato in mensaje:
    #Con el método send, enviamos el mensaje
    clientSocket.send(mensaje.encode())
    #Cerramos la instancia del objeto servidor
    clientSocket.close()
    #Imprimimos la palabra Adios para cuando se cierre la conexion
    print("Conexión cerrada")
"""
"""
def serial_read():
    ser = serial.Serial('/dev/ttyACM0', 115200)  # open serial port
    print(ser.name)                              # check which port was r$
    lista_de_datos = []
    datos_a_enviar = []
    AC0 = "000318"                               # chequeo si el Sensor r$
    while 1:
        line = ser.readline().decode(encoding = "utf-8")     # write a stri$
        new_line = (line[:-2])
        if (new_line == AC0):
            i = 4
            while i >= 0:
                comando = ser.readline().decode(encoding = "utf-8")  # Esto deb$
                new_comando = comando[:-2]
                print(new_comando)
                line = ser.readline().decode(encoding = "utf-8")     # write a $
                new_line = (line[:-2])
                lista_de_datos = new_line.split("+")
                for datos in lista_de_datos:
                    datos_a_enviar.append(datos)
                print(datos_a_enviar)
                i = i - 1

"""
def run():
    ser = serial.Serial('/dev/ttyACM0', 115200)  # open serial port
    print(ser.name)                              # check which port was r$
    lista_de_datos = []
    datos_a_enviar = []
    AC0 = "000318"                               # chequeo si el Sensor r$
    while 1:
        line = ser.readline().decode(encoding = "utf-8")     # write a stri$
        new_line = (line[:-2])
        if (new_line == AC0):
            i = 4
            while i >= 0:
                comando = ser.readline().decode(encoding = "utf-8")  # Esto deb$
                new_comando = comando[:-2]
                print(new_comando)
                line = ser.readline().decode(encoding = "utf-8")     # write a $
                new_line = (line[:-2])
                lista_de_datos = new_line.split("+")
                for datos in lista_de_datos:
                    datos_a_enviar.append(datos)
                print(datos_a_enviar)
                i = i - 1
            cadena_a_enviar = ",".join(datos_a_enviar)
            client = connect_mqtt()
            # client.loop_start()
            publish(client, cadena_a_enviar)
            # new_publish()
            # msgs = tuple(lista)
            # publish.multiple(msgs, broker)
            datos_a_enviar = []

if __name__ == '__main__':
    run()
