# Makefile

SHELL := sh -e

all: test build

test:
	@echo " Hecho!"

build:
	@echo "Nada para compilar!"


install:

	mkdir -p $(DESTDIR)/usr/share/canaima-notas-gnome/.notas/
	mkdir -p $(DESTDIR)/usr/share/applications/
	mkdir -p $(DESTDIR)/usr/bin/

	cp -r scripts/canaima-notas-gnome.py captcha $(DESTDIR)/usr/share/canaima-notas-gnome/
	cp desktop/canaima-notas-gnome.desktop $(DESTDIR)/usr/share/applications/
	cp scripts/canaima-notas-gnome.sh  $(DESTDIR)/usr/bin/canaima-notas-gnome
	
uninstall:

	rm -rf $(DESTDIR)/usr/share/canaima-notas-gnome/
	rm -rf $(DESTDIR)/usr/bin/canaima-notas-gnome
	
clean:

distclean:

reinstall: uninstall install
