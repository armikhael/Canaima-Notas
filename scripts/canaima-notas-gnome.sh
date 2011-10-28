#!/bin/bash

cd /usr/share/canaima-notas-gnome/
if [ -e /usr/share/canaima-notas-gnome/.notas ]
then
	python canaima-notas-gnome.py
fi
