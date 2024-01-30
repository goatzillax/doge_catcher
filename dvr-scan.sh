#!/usr/bin/bash

FN=$1
#  why the fuck does this not exist in UNIX already
DN=`dirname $FN`
TEMP=`basename $FN .mp4`
BN=$DN/$TEMP

ffmpeg -y -i $FN -c:v huffyuv $BN-temp.avi

#dvr-scan -i temp.avi -a 849 60 1559 78 1549 141 1510 147 1485 199 868 177 -o $BN.avi --logfile $BN.log
dvr-scan -i $BN-temp.avi -a 859 70 1207 70 1554 100 1552 136 1504 136 1485 191 867 167 -t 0.30 -o $BN.avi --logfile $BN.log

rm $BN-temp.avi
