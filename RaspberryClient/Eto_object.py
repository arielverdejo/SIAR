#!/usr/bin/env python3
class EtoObject:

  def read_Eto(self):
    """Lee un valor desde un archivo y lo devuelve"""
    with open("valor_Eto") as f:
      valor = f.readline()
    return valor

  def saludar(self):
    """Imprime un saludo en pantalla."""
    print("¡Hola, mundo!")

