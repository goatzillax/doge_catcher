#!/bin/bash

FN=$1
DN=`dirname $1`
BN=`basename $1 .filter`

if [ ! -f "${FN}" ]; then
   echo suck on it trebeck
   exit
fi

ffmpeg -i ${DN}/${BN}.mp4 -filter_complex_script ${DN}/${BN}.filter -vsync 0 ${DN}/${BN}-frame%04d.png

for f in `ls ${DN}/$BN-frame????.png`; do
   python findContours.py $f
done
