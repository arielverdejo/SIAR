#!/usr/bin/env python3

import serial
import socket

#Variables
host = '192.168.0.104'
port = 8050


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
      i = 3
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
      enviar_datos(mensaje)
      print(mensaje)
      mensaje = ""

def main():
  serial_read()

if __name__ == "__main__":
  main()