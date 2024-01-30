#/bin/bash

FN=$1

START=$2
END=$3

if [ ! -f "$FN" ]; then
	echo suckit
	exit
fi

BN=`basename $FN .mp4`

ffmpeg -i $FN -vf "select=between(n\,${START}\,${END})" -vsync 0 ${BN}-frame%04d.png
