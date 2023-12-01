#!/bin/bash

BN=$1

if [ ! -f "${BN}.filter" ]; then
   echo suck on it trebeck
   exit
fi

ffmpeg -i ${BN}.mp4 -filter_complex_script ${BN}.filter -vsync 0 ${BN}-frame%04d.png

for f in `ls $BN-frame????.png`; do
   python ./findContours.py $f
done
