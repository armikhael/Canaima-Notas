#!/bin/bash

APP_DIR=/usr/share/canaima-notas-gnome/scripts/

if [ -e $APP_DIR ]
then
	cd $APP_DIR
	python canaima-notas-gnome.py
fi
