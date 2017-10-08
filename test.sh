#!/bin/bash

v4l2-ctl --set-ctrl=exposure_auto=1
v4l2-ctl --set-ctrl=exposure_absolute=100
v4l2-ctl --set-ctrl=white_balance_temperature_auto=0
v4l2-ctl --set-ctrl=white_balance_temperature=0
v4l2-ctl --set-ctrl=saturation=150
v4l2-ctl --set-ctrl=brightness=126
v4l2-ctl --set-ctrl=gain=0
v4l2-ctl --set-ctrl=contrast=0

