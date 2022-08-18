#!/bin/bash
netcat -z -w 10 siardb.frm.utn.edu.ar 3306
if [ $? -eq 0 ]
then
        echo -n `date '+%Y-%m-%d %H:%M > '` >> /home/pi/Documents/Logs/connectivity.log
        echo " OK    conectividad a siardb" >> /home/pi/Documents/Logs/connectivity.log
else
        echo -n `date '+%Y-%m-%d %H:%M > '` >> /home/pi/Documents/Logs/connectivity.log
        echo " ERROR conectividad a siardb" >> /home/pi/Documents/Logs/connectivity.log
fi
netcat -z -w 10 google.com 80
if [ $? -eq 0 ]
then
        echo -n `date '+%Y-%m-%d %H:%M > '` >> /home/pi/Documents/Logs/connectivity.log
        echo " OK    conectividad a google" >> /home/pi/Documents/Logs/connectivity.log
else
        echo -n `date '+%Y-%m-%d %H:%M > '` >> /home/pi/Documents/Logs/connectivity.log
        echo " ERROR conectividad a google" >> /home/pi/Documents/Logs/connectivity.log
fi
