#!/usr/bin/env python3

import socket
import time
import datetime
import re
import mysql.connector

def insert_database(lista_de_datos):
    """This function insert a list into the database."""
    database_connect = {
        "host":"localhost",
        "user":"root",
        "password":"ariel",
        "database":"testDB"
    }

    time_stamp = time.time()
    timestamp_day = datetime.datetime.fromtimestamp(time_stamp)
    timestamp_hour = datetime.datetime.utcnow()

    conexion = mysql.connector.connect(**database_connect)
    cursor = conexion.cursor()

    sql_insert = (
        "INSERT INTO tester("
        "solar,precipitation,"
        "strikes,strikesDistance,"
        "windSpeed,windDirection,gustWindSpeed,"
        "airTemperature,vaporPressure,atmosphericPressure,"
        "relativeHumidity,humiditySensorTemperature,"
        "xOrientation,yOrientation,"
        "NorthWindSpeed,EastWindSpeed,"
        "dia,hora) "

        "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    )
    data = (
        str(lista_de_datos[2]),str(lista_de_datos[3]),
        str(lista_de_datos[4]),str(lista_de_datos[5]),
        str(lista_de_datos[7]),str(lista_de_datos[8]),str(lista_de_datos[9]),
        str(lista_de_datos[11]),str(lista_de_datos[12]),str(lista_de_datos[13]),
        str(lista_de_datos[14]),str(lista_de_datos[15]),
        str(lista_de_datos[17]),str(lista_de_datos[18]),
        str(lista_de_datos[21]),str(lista_de_datos[22]),
        timestamp_day, timestamp_hour
    )
    cursor.execute(sql_insert,data)
    conexion.commit()
    cursor.close()
    conexion.close()

def especial_split(string_to_split):
    """Convert a string with + and - to a list with element, which conservates
    the sign + or -."""
    separador = ","
    string_with_plus = string_to_split.replace("+",",+")
    string_final = string_with_plus.replace("-",",-")
    regular_exp = '|'.join(map(re.escape, separador))
    return re.split(regular_exp, string_final)

def server_conexion():
    """This function makes the connection with the server."""
    port = 8050

    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the port
    server_address = ("", port)
    print(F"Starting up on {server_address[0]} port {server_address[1]}")
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
            print(F"Received: \n{data}")
            datos_en_lista = especial_split(data)
            print(datos_en_lista)
            insert_database(datos_en_lista)
        finally:
            # Clean up the connection
            connection.close()

def main():
    server_conexion()

if __name__ == "__main__":
    main()
