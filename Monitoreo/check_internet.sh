#!/bin/bash

# Este script utiliza la función check_internet para comprobar la conexión a Internet.
# La función envía un paquete de ping a google.com y si recibe una respuesta, devuelve 0, lo que indica que hay conexión a Internet.
# Si no se recibe una respuesta, devuelve 1, lo que indica que no hay conexión a Internet.

# Luego, el script utiliza un bucle while para comprobar la conexión a Internet.
# Si no se detecta conexión a Internet, el script espera 10 segundos y luego vuelve a intentarlo.
# Si después de 5 intentos no se detecta conexión a Internet, el script reinicia el equipo utilizando el comando sudo reboot.

# Para utilizar este script, guárdalo en un archivo con el nombre que desees, por ejemplo check-internet.sh,
# y luego hazlo ejecutable con el comando chmod +x check-internet.sh. Después, simplemente ejecuta el script con el comando ./check-internet.sh.

# Función para comprobar la conexión a Internet
check_internet() {
  if ping -q -c 1 -W 1 google.com >/dev/null; then
    return 0
  else
    return 1
  fi
}

# Contador de intentos
tries=1

# Comprobar la conexión a Internet
while ! check_internet; do
  echo -n `date '+%Y-%m-%d %H:%M > '` >> /home/pi/Documents/Logs/internet.txt
  echo "Intento $tries: No se detectó conexión a Internet." >> /home/pi/Documents/Logs/internet.txt

tries=$((tries+1))
  if [ $tries -gt 5 ]; then
    echo -n `date '+%Y-%m-%d %H:%M > '` >> /home/pi/Documents/Logs/internet.txt
    echo "No hay conexión a Internet después de 5 intentos. Reiniciando..." >> /home/pi/Documents/Logs/internet.txt
    sudo reboot
  else
    sleep 30
  fi
done

echo "Conexión a Internet detectada."
