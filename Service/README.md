Para configurar nuestra raspberry creamos tres servicios que se ejecutan al iniciar la misma.
Estos tres servicios son:
gateway_init_SIAR.service  
gprs_init_SIAR.service  
python_SIAR.service

Los archivos deben ser colocados en

/lib/systemd/system  

Estos archivos deben tienen scripts asociados a que se encuentran a continuacion
script_gateway.sh
script_gprs.sh
y el de python

Todos los archivos deben tener permiso de ejecucion



