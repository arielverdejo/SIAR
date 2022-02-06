#!/usr/bin/env python3

import serial
import socket

import socket
import time
import datetime
import re
import mysql.connector

#Variables
host = '192.168.0.101'
port = 8050

def insert_database(lista_de_datos):
  """This function insert a list into the database."""
  database_connect = {
    "host":"192.168.0.101",
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

def enviar_datos(mensaje):
  # Creación de un objeto socket (lado cliente)
  clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  # Conexión con el servidor. Parametros: IP (puede ser del tipo 192.168.1.1 o localhost), Puerto
  clientSocket.connect((host, port))
  print("Conectado al servidor")
  clientSocket.send(mensaje.encode())
  # Cerramos la instancia del objeto servidor
  clientSocket.close()
  # Imprimimos mensaje  para cuando se cierre la conexion
  print("Conexión cerrada")

def serial_read():
  lista_de_datos = []
  datos_a_enviar = []
  mensaje = "0"
  # sequence = 0
  # Variable utilizada para saber si el sensor responde a AC0
  AC0 = "000318"

  # Open serial port
  serie = serial.Serial('/dev/ttyACM0', 115200)
  # Check port
  print(serie.name)

  while 1:
    # Read a line of Serial Port
    line = serie.readline().decode(encoding = "utf-8")
    # Take off the first two elements
    new_line = (line[:-2])
    if (new_line == AC0):
      i = 4
      while i >= 0:
        # Read the new line en este caso un comandos
        comando = serie.readline().decode(encoding = "utf-8")
        new_comando = comando[:-2]
        print(new_comando)
        # Read datos
        line = serie.readline().decode(encoding = "utf-8")
        # Quito los primeros datos que no pertenecen a datos utiles
        new_line = (line[:-2])
        print(mensaje)
        mensaje = mensaje + "+" + new_line
        i = i - 1

      #sequence += 1
      #print(sequence)
      #mensaje = str(sequence) + mensaje
      #enviar_datos(mensaje)
      print(mensaje)
      datos_en_lista = especial_split(mensaje)
      print(datos_en_lista)
      insert_database(datos_en_lista)
      mensaje = "0"

def main():
  serial_read()

if __name__ == "__main__":
  main()