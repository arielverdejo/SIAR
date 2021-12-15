# SIAR
La principal función del proyecto es leer desde una estación datos usando el protocolo SDI-12 y publicarlo en la Web

## Carpetas

El proyecto consta de tres comunicaciones
1. Arduino - Sensor SDI-12
En la carpeta Arduino estaran los softwares que se encargaran de esta tarea
2. Arduino - Raspberry Publisher
En la carpeta Raspberry Publisher se encontrara el código encargado de tomar los datos desde el Arduino y enviarlos a la Raspberry encargada de presentar los datos.
3. Raspberry Publisher - Raspberry Subscriber
En la carpeta Raspberry Subscriber se encontrara el código encargado de recibir los datos enviados por la Raspberry Publisher y mostrarlos. 
