# Makefile

SHELL := sh -e
PYCS = $(shell find . -type f -iname "*.pyc")
IMAGES = $(shell ls -1 img/ | grep "\.svg" | sed 's/\.svg//g')
CONVERT = $(shell which convert)

SCRIPTS = "debian/preinst install" "debian/postinst configure" "debian/prerm remove" "debian/postrm remove"

all: test build

test:
	@echo " Hecho!"


build: gen-img

gen-img: clean-img

	@printf "Generando imágenes desde las fuentes [SVG > PNG,JPG] ["
	@for IMAGE in $(IMAGES); do \
		$(CONVERT) -background None img/$${IMAGE}.svg img/$${IMAGE}.png; \
		printf "."; \
	done;
	@printf "]\n"

clean-img:

	@printf "Cleaning generated images [JPG,PNG] ["
	@for IMAGE in $(IMAGES); do \
		rm -rf img/$${IMAGE}.png; \
		printf "."; \
	done
	@printf "]\n"

clean-pyc:

	@printf "Cleaning precompilated python files ["
	@for PYC in $(PYCS); do \
		rm -rf $${PYC}; \
		printf "."; \
	done
	@printf "]\n"

install:
	# Installing shared data
	mkdir -p $(DESTDIR)/usr/share/canaima-notas-gnome/
	mkdir -p $(DESTDIR)/usr/bin/
	mkdir -p $(DESTDIR)/usr/share/applications/
	mkdir -p $(DESTDIR)/usr/share/gnome/help

	cp -r canaima_notas_gnome.py $(DESTDIR)/usr/share/canaima-notas-gnome
	cp -r img $(DESTDIR)/usr/share/canaima-notas-gnome/	
	rm -rf $(DESTDIR)/usr/share/canaima-notas-gnome/img/*.svg
	cp -r desktop/canaima-notas-gnome.desktop $(DESTDIR)/usr/share/applications/
	cp -r ayuda/canaima-notas-gnome $(DESTDIR)/usr/share/gnome/help
	ln -s /usr/share/canaima-notas-gnome/scripts/canaima-notas-gnome.py $(DESTDIR)/usr/bin/canaima-notas-gnome

uninstall:

	# Uninstalling shared data
	
	rm -rf $(DESTDIR)/usr/share/canaima-notas-gnome/
	rm -rf $(DESTDIR)/usr/share/applications/canaima-notas-gnome.desktop
	rm -rf $(DESTDIR)/usr/share/gnome/help/canaima-notas-gnome
	
	# Uninstalling executables
	rm -rf $(DESTDIR)/usr/bin/canaima-notas-gnome
clean:

distclean:

reinstall: uninstall install
