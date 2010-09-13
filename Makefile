# Makefile

install:
	# Installing shared data
	mkdir -p $(DESTDIR)/usr/share/canaima-notas/
	cp -r canaima-notas.png canaima-notas.glade $(DESTDIR)/usr/share/canaima-notas/

	# Installing executables
	mkdir -p $(DESTDIR)/usr/bin/
	cp canaima-notas  $(DESTDIR)/usr/bin/

	# Installing documentation
	#mkdir -p $(DESTDIR)/usr/share/doc/canaima-semilla
	#cp AUTHORS CREDITS README $(DESTDIR)/usr/share/doc/canaima-semilla/

	
uninstall:
	# Uninstalling shared data
	rm -rf $(DESTDIR)/usr/share/canaima-notas/
	
	# Uninstalling executables
	rm -f $(DESTDIR)/usr/bin/canaima-notas

	# Uninstalling documentation
	#rm -rf $(DESTDIR)/usr/share/doc/canaima-semilla/

	
clean:

distclean:

reinstall: uninstall install
