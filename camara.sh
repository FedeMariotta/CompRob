#!/bin/bash
v4l2-ctl -c brightness=250
v4l2-ctl -c contrast=28
v4l2-ctl -c saturation=80
v4l2-ctl -c white_balance_temperature_auto=0
v4l2-ctl -c gamma=90
v4l2-ctl -c white_balance_temperature=2900
v4l2-ctl -c exposure_auto_priority=0
v4l2-ctl --list-ctrls-menus

# Set exposure_auto (menu): min=0 max=3 default=1
#                               1: Manual Mode
#                               3: Aperture Priority Mode
v4l2-ctl -c exposure_auto=1


#while [ $EXPOSURE -lt 20000 ]
#do
#  echo $EXPOSURE
#  v4l2-ctl -c exposure_absolute=$EXPOSURE
#  EXPOSURE=$[$EXPOSURE+2]
#  sleep 0.1
#done

