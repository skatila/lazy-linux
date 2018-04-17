#!/bin/sh
###############################################################################
# Copyright (C) 2018 by Sabin Katila (sabin@sabink.org)                       #
# Released under the terms of GPLv3                                           #
# <http://www.gnu.org/licenses/                                               #
# You are free to use, modify and/or redistribute as per the terms of GPL v3  #
#                                                                             #
###############################################################################
# Mapping my regular mouse for left handed use
# Mapping my wireless logitech keyboard's trackpad for righthanded use
# Fine tuned controlled over how every input device works!!!
# Thank you xinput!!!!!

# This is needed since mouse is mapped for right hand
DEV_LOGI=$(xinput list | grep 'Logitech' | grep pointer  | tr [:space:] '\n'  | grep ^id | cut -d '=' -f2)
DEV_DELL=$(xinput list | grep 'Dell Dell USB Mouse' | grep pointer  | tr [:space:] '\n'  | grep ^id | cut -d '=' -f2)

#xinput set-button-map "pointer:Logitech K400"  3 2 1 4
if [ ${DEV_LOGI:+1} ];then
	echo "Setting for Logitech"
	xinput set-button-map $DEV_LOGI 1 2 3 4
fi

if [ ${DEV_DELL:+1} ];then
	echo "Setting for Dell Dell USB Mouse"
	xinput set-button-map $DEV_DELL 3 2 1 4
fi
