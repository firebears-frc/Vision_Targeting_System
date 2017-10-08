#!/bin/bash


while true; do
	if  lsusb | grep -q Webcam
		then
		python /home/pi/Desktop/VisionTargetingSystem/
		break
	fi

done

sh test.sh
sh test.sh
