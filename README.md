# SIAR
La principal función del proyecto es leer datos desde una estación meteorológica ATMOS 41 usando el protocolo SDI-12 para luego publicar estos mismos en la Web.
La publicación se realizara a traves de la plataforma Grafana y una página WEB. También se publicará el cálculo de la Evapotranspiración mediante un bot de Telegram.

## Esquema de comunicaciones del proyecto

En la siguiente imagen se puede ver el esquema de conexionado.

![Esquema de conexionado del proyecto](https://github.com/arielverdejo/SIAR/blob/main/Esquema-SIAR.png)

Basicamente el proyecto cuenta con cinco equipos. Los cuales son servidor WEB, una Raspberry Pi, un Arduino UNO, un Modem GPRS y una estación meteorologica ATMOS 41.

El servidor WEB se encuentra alojado fisicamente en la Universidad Tecnológica Nacional Facultad Regional Mendoza.
En el se encuentra la base de datos por lo tanto es quien recibe los datos enviados por la Raspberry Pi. También aloja el software Grafana quien muestra los valores recibidos. En este también se encuentra corriendo el software que controla el bot de Telegram.

La Raspberry Pi recibe los datos del Arduino UNO, los procesa y los envia a tráves de internet hacia el servidor WEB. La conexión con internet se logra con el Modem GPRS. Este equipo realiza el calculo de la Evapotranspiración.

El Arduino UNO recibe los datos de la estación Meteorológica y los envia a la Raspberry Pi. Entre medio de estos equipos existe un adaptador de señales que permite la comunicación con el protocolo SDI-12.

La estación Meteorológica ATMOS 41 realiza la toma de todos los parametros y los envia al Arduino UNO.
 
## Carpetas

### Breve descripción de las carpetas y sus contenidos.

Actualmente tenemos siete carpetas las cuales contendran archivos referidos a un tema.

#### Arduino
La carpeta Arduino contrendra el programa que se utiliza para obtener los datos desde la estación ATMOS 41.
Además contendra la descripción del mismo al igual que un esquema del adaptador utilizado para realizar dicha comunicación.

#### Database
En esta carpeta estara la forma en que se implemento dicho base de datos en el servidor.

#### Monitoreo
Esta carpeta contiene diferentes scripts que posibilitaron la depuración del software y que actualmente corren en la Raspberry Pi.

#### No-IP
Debido a que la Raspberry Pi no posee una IP Pública es que debemos usar este software para realizar tareas remotas.
En esta carpeta se encontraran detalles de este software y como su instalación y datos de acceso.

#### RaspberryClient
Carpeta que contiene el software encargado de tomar los datos desde el Arduino y enviarlos al servidor.
Asi como tambien el software encargado de realizar el caluculo del valor de Evapotranspiración.
Tambien existe un archivo que se utiliza para almacenar dicho valor.

#### Server
Esta carpeta contendra las configuraciones realizadas en el servidor y ademas el software del chat-bot de Telegram.

#### Service
Esta carpeta almacenara los servicios generados para que se inicien los programas en la Raspberry Pi.

## Comunicaciones

El proyecto consta de tres comunicaciones
1. Arduino - Sensor SDI-12

En la carpeta Arduino estaran los softwares que se encargaran de esta tarea

2. Arduino - Raspberry

En la carpeta RaspberryClient se encontrara el código encargado de tomar los datos desde el Arduino y enviarlos al Servidor que sera el encargado de presentar los datos.

3. Raspberry - Server

En la carpeta Server se encontrara el código encargado de recibir los datos enviados por la Raspberry y mostrarlos. 
