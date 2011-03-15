# Makefile

SHELL := sh -e

all: test build

test:
	@echo " Hecho!"

build:
	@echo "Nada para compilar!"


install:
	# Installing shared data
	mkdir -p $(DESTDIR)/usr/share/canaima-notas/
	mkdir -p $(DESTDIR)/usr/share/canaima-notas/.notas/
	mkdir -p $(DESTDIR)/usr/share/applications/

	cp Canaima-Notas.py AUTHORS COPYING README THANKS  $(DESTDIR)/usr/share/canaima-notas/
	cp -R catpcha/  $(DESTDIR)/usr/share/canaima-notas/
	cp canaima-notas.desktop $(DESTDIR)/usr/share/applications/

	# Installing executables
	mkdir -p $(DESTDIR)/usr/bin/
	cp canaima-notas  $(DESTDIR)/usr/bin/
	
uninstall:
	# Uninstalling shared data
	rm -rf $(DESTDIR)/usr/share/canaima-notas/
	
	# Uninstalling executables
	rm -rf $(DESTDIR)/usr/bin/canaima-notas
	
clean:

distclean:

reinstall: uninstall install
