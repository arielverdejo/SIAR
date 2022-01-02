#!/usr/bin/env python3

import socket
import sys
import mysql.connector
import time
import datetime
import re

def insertDB(listadedatos):
    
    dbConnect = {
        "host":"localhost",
        "user":"root",
        "password":"ariel",
        "database":"testDB"
    }

    ts = time.time()
    timestamp_day = datetime.datetime.fromtimestamp(ts)
    timestamp_hour = datetime.datetime.utcnow()

    conexion = mysql.connector.connect(**dbConnect)
    cursor = conexion.cursor()

    sqlInsertar = (
        "INSERT INTO tester(solar,precipitation,strikes,strikesDistance,"
                            "windSpeed,windDirection,gustWindSpeed,"
                            "airTemperature,vaporPressure,atmosphericPressure,relativeHumidity,humiditySensorTemperature,"
                            "xOrientation,yOrientation,"
                            "NorthWindSpeed,EastWindSpeed,"
                            "dia,hora) "

        "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    )
    
    data = (str(listadedatos[2]),str(listadedatos[3]),str(listadedatos[4]),str(listadedatos[5]),
            str(listadedatos[7]),str(listadedatos[8]),str(listadedatos[9]),
            str(listadedatos[11]),str(listadedatos[12]),str(listadedatos[13]),str(listadedatos[14]),str(listadedatos[15]),
            str(listadedatos[17]),str(listadedatos[18]),
            str(listadedatos[21]),str(listadedatos[22]),
            timestamp_day, timestamp_hour)
    
    cursor.execute(sqlInsertar,data)
    conexion.commit()
    cursor.close()
    conexion.close()

def especial_split(string_to_split):
    separador = ","
    string_with_plus = string_to_split.replace("+",",+")
    string_final = string_with_plus.replace("-",",-")
    regular_exp = '|'.join(map(re.escape, separador))
    return re.split(regular_exp, string_final)

def server_conexion():
    port = 8050

    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the port
    server_address = ("", port)
    print('Starting up on {} port {}'.format(*server_address))
    sock.bind(server_address)

    # Listen for incoming connections
    sock.listen(1)

    while True:
        # Wait for a connection
        print('Waiting for a connection')
        connection, client_address = sock.accept()
        try:
            print('Connection from', client_address)

            # Receive the data in small chunks and retransmit it
            data = connection.recv(1024).decode("utf-8")
            print('Received: \n{!r}'.format(data))
            datos_en_lista = especial_split(data)
            print(datos_en_lista)
            #datos_en_lista = [1,2,3,4]
            insertDB(datos_en_lista)
                
        finally:
            # Clean up the connection
            connection.close()

def main():
  server_conexion()

if __name__ == "__main__":
  main()