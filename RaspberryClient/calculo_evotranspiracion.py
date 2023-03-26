#!/usr/bin/env python3

import math
import datetime
import statistics
import mysql.connector

def calculos_sensor():
  temperatura = []
  humedad = []
  presionAtmosferica = []
  velocidadViento = []
  numero_dia = 0
  PA = 0
  TM = 0
  Tm = 0 
  HR_M = 0
  HR_m = 0 
  uviento = 0

  database_connect = {
    "host":"200.10.196.116",
    "user": "pi",
    "password": "raspberry",
    "database":"testDB"
  }

  try:
    cnx = mysql.connector.connect(**database_connect)
    cursor = cnx.cursor()

    query = ("SELECT airTemperature, relativeHumidity, atmosphericPressure, windSpeed FROM tester "
              "WHERE dia BETWEEN %s AND %s")

    hoy = datetime.date.today()
    #hoy = datetime.datetime(year=2022, month=5,day=13)
    ayer = hoy - datetime.timedelta(days=1)

    cursor.execute(query,(ayer,ayer))

    for (airTemperature,relativeHumidity,atmosphericPressure,windSpeed) in cursor:
      temperatura.append(airTemperature)
      humedad.append(relativeHumidity)
      presionAtmosferica.append(atmosphericPressure)
      velocidadViento.append(windSpeed)
    
    TM = max(temperatura)
    Tm = min(temperatura)
    HR_M = max(humedad)
    HR_m = min(humedad)
    PA = statistics.mean(presionAtmosferica)
    uviento = statistics.mean(velocidadViento)
    numero_dia = (ayer - datetime.date(hoy.year, 1, 1)).days + 1
    #numero_dia = (ayer - datetime.datetime(hoy.year,1,1)).days + 1

  except mysql.connector.Error as error:
    print("Failed calculos sensor")

  finally:
    if cnx.is_connected():
      cnx.commit()
      cursor.close()
      cnx.close()
  
  return [numero_dia, PA, TM, Tm, HR_M, HR_m, uviento] 

def valores_intensidad_solar(inicio, fin):
  sol = []

  database_connect = {
    "host":"200.10.196.116",
    "user": "pi",
    "password": "raspberry",
    "database":"testDB"
  }

  try:
    cnx = mysql.connector.connect(**database_connect)
    cursor = cnx.cursor()

    query = ("SELECT solar FROM tester "
            "WHERE hora BETWEEN %s AND %s")

    cursor.execute(query, (inicio, fin))

    for (solar) in cursor:
      sol.append(solar)

  except mysql.connector.Error as error:
    print("Failed tiempo_por_cuartos")

  finally:
    if cnx.is_connected():
      cnx.commit()
      cursor.close()
      cnx.close()

  return sol

def calculo_radiacion_por_minuto(inicio, fin):
  valores_radiacion_en_lista = valores_intensidad_solar(inicio, fin)
  suma_radiacion = 0
  for element in valores_radiacion_en_lista:
    radiacion_por_minuto = int(element[0]) * 60
    suma_radiacion += radiacion_por_minuto
  print("Radiacion total por cuarto = {}".format(suma_radiacion))

  return suma_radiacion

def calculo_radiacion_solar():
  hoy = datetime.datetime.today()
  #hoy = datetime.datetime(year=2022, month=5,day=13)

  ayer = hoy - datetime.timedelta(days=1)
  ayer_inicial = ayer.replace(hour=0, minute=0, second=0, microsecond=0) + datetime.timedelta(hours=3)
  hoy_final = hoy.replace(hour=0, minute=0, second=0, microsecond=0) + datetime.timedelta(hours=3)

  Rs_real = ((calculo_radiacion_por_minuto(ayer_inicial, hoy_final))
    /1000000)
  
  print(Rs_real)

  return Rs_real

def guardar_en_archivo(dato):
  with open("/home/pi/SIAR/RaspberryClient/valor_Eto",'w') as f:
    f.write(str(dato))

def obtener_valores_sensor():
  valores_obtenidos = calculos_sensor()

  Altura =  920                                                            #B
  LatGrad = 33                                                             #C Datos fijos que se deben buscar
  LatRad = math.pi * LatGrad/180                                           #D
  dl = valores_obtenidos[0]                                                #E
  dr = 1+0.033*math.cos(2*math.pi/365*dl)                                  #F 
  delta = 0.409*math.sin(2*math.pi/365*dl-1.39)                            #G
  ws = math.acos(-math.tan(LatRad)*math.tan(delta))                        #H
  sen_sen = math.sin(LatRad)*math.sin(delta)                               #I
  cos_cos = math.cos(LatRad)*math.cos(delta)                               #J
  Gsc = 0.082                                                              #K
  Ra = 24*60/math.pi*Gsc*dr*(ws*sen_sen+cos_cos*math.sin(ws))              #L
  N =24/math.pi*ws                                                         #M
  n = N                                                                    #N cantidad de tiempo con radiacion solar
  Rs_cal = (0.25 + 0.5*(n/N))*Ra                                           #O
  Rs_real = calculo_radiacion_solar()                                      #P
  Rso_despejado = (0.75+2*10**(-5)*Altura)*Ra                              #Q
  Evaporacion = 0.408*Rs_real                                              #R
  Sigma =(4.903)*10**(-9)                                                  #S
  Lambda = 2.45                                                            #T
  cp = 1.013*10**(-3)                                                      #U
  Epsilon = 0.622                                                          #V
  PA_Atmos = valores_obtenidos[1]                                          #Y
  Ganma = cp*PA_Atmos/(Epsilon*Lambda)                                     #W
  TM_Atmos = valores_obtenidos[2]                                          #Z
  Tm_Atmos = valores_obtenidos[3]                                          #AA
  PA = (101.3*((((TM_Atmos+Tm_Atmos)/2+273.16)-0.0065*Altura)/
      ((TM_Atmos+Tm_Atmos)/2+273.16))**5.26)                               #X
  ea = 2.1                                                                 #AB
  HR_M_Atmos = valores_obtenidos[4]                                        #AC
  HR_m_Atmos = valores_obtenidos[5]                                        #AD
  es_TM = 0.6108*math.e**(17.27*TM_Atmos/(TM_Atmos+237.3))                 #AE
  es_Tm = 0.6108*math.e**(17.27*Tm_Atmos/(Tm_Atmos+237.3))                 #AF
  ea_M = es_TM*HR_m_Atmos                                                  #AG
  ea_m = es_Tm*HR_M_Atmos                                                  #AH
  es_ea = (es_TM+es_Tm)/2-(ea_M+ea_m)/2                                    #AI
  Rs_Rso = Rs_real/Rso_despejado                                           #AJ
  Rnl = (Sigma *((((TM_Atmos+273.16)**4+(Tm_Atmos+273.16)**4))/2)
    *(0.34-0.14*math.sqrt((ea_M+ea_m)/2))
    *(1.35*Rs_real/Rso_despejado-0.35))                                    #AK
  Rns = (1-0.23)*Rs_real                                                   #AL
  Rn_calc = Rns-Rnl                                                        #AM
  Rn = Rn_calc*0.408                                                       #AN
  G = 0                                                                    #AO
  AlturaAnem = 2                                                           #AP
  uviento_Atmos = valores_obtenidos[6]                                     #AQ
  uvientocor = uviento_Atmos*(4.87/(math.log(67.8*AlturaAnem-5.42)))       #AR
  Delta_Mayuscula = ((4098*(0.6108*math.e**((17.27*((TM_Atmos+Tm_Atmos)/2)
                  /((TM_Atmos+Tm_Atmos)/2+237.3)))))
                  /(((TM_Atmos+Tm_Atmos)/2+237.3)**2))                     #AS
  Eto = ((Rn*(Delta_Mayuscula)/(Delta_Mayuscula+Ganma*(1+0.34*uvientocor)))+
      ((900/((TM_Atmos+Tm_Atmos)/2+273)*uvientocor*(es_ea)*Ganma)
      /(Delta_Mayuscula+Ganma*(1+0.34*uviento_Atmos))))                    #AT


  Parametros = ([Altura,LatGrad,LatRad,dl,dr,delta,ws,sen_sen,cos_cos,Gsc,Ra,
              N,n,Rs_cal,Rs_real,Rso_despejado,Evaporacion,Sigma,Lambda,cp,
              Epsilon,Ganma,PA,PA_Atmos,TM_Atmos,Tm_Atmos,ea,HR_M_Atmos,
              HR_m_Atmos,es_TM,es_Tm,ea_M,ea_m,es_ea,Rs_Rso,Rnl,Rns,Rn_calc,
              Rn,G,AlturaAnem,uviento_Atmos,uvientocor,Delta_Mayuscula,Eto])
  
  guardar_en_archivo(Eto)

def main():
  obtener_valores_sensor()

if __name__ == "__main__":
  main()

"""
Calcular
- dias dl #E
- radiacion solar Rs_real #P
- Presion Atmosferica PA #Y x
- Temperatura Maxima TM #Z x
- Temperatura Minima Tm #AA x
- Humedad Relativa Maxima HR_M #AC x
- Humedad Relativa Minima HR_m #AD x
- Viento uviento #AQ x
"""