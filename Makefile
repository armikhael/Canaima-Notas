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
	cp canaima-notas.png arriba2.png canaima-notas.glade canaima-notas.desktop canaima-notas.py  $(DESTDIR)/usr/share/canaima-notas/
	cp canaima-notas.desktop $(DESTDIR)/usr/share/applications/

	# Installing executables
	mkdir -p $(DESTDIR)/usr/bin/
	cp canaima-notas-bin  $(DESTDIR)/usr/bin/

	# Installing documentation
		
uninstall:
	# Uninstalling shared data
	rm -rf $(DESTDIR)/usr/share/canaima-notas/
	
	# Uninstalling executables
	rm -rf $(DESTDIR)/usr/bin/canaima-notas-bin

	# Uninstalling documentation
	

	
clean:

distclean:

reinstall: uninstall install
