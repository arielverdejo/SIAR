#!/bin/bash
netcat -z -w 10 siardb.frm.utn.edu.ar 3306
if [ $? -eq 0 ]
then
        echo -n `date '+%Y-%m-%d %H:%M > '` >> /tmp/connectivity.log
        echo " OK    conectividad a siardb" >> /tmp/connectivity.log
else
        echo -n `date '+%Y-%m-%d %H:%M > '` >> /tmp/connectivity.log
        echo " ERROR conectividad a siardb" >> /tmp/connectivity.log
fi
netcat -z -w 10 google.com 80
if [ $? -eq 0 ]
then
        echo -n `date '+%Y-%m-%d %H:%M > '` >> /tmp/connectivity.log
        echo " OK    conectividad a google" >> /tmp/connectivity.log
else
        echo -n `date '+%Y-%m-%d %H:%M > '` >> /tmp/connectivity.log
        echo " ERROR conectividad a google" >> /tmp/connectivity.log
fi
