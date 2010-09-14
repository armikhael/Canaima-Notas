#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
import os
import sys
try:		 
        import threading, locale
        import gobject       
        import vte
	import webbrowser	
 	import pygtk
  	pygtk.require("2.0")
except:
  	pass
try:
	import gtk
  	import gtk.glade
except:
	sys.exit(1)
	
	

class nota_canaima:
	"""cliente de notas.canaima.softwarelibre.gob.ve"""

	def __init__(self):
		
		#Se define el archivo .glade en el cual se basa la GUI.
		#self.gladefile = "canaima-notas.glade"
		self.gladefile = "/usr/share/canaima-notas/canaima-notas.glade"
		self.widgets = gtk.glade.XML(self.gladefile)
		
		#Se conectan las señales basicas de los botones de la GUI de Glade a funciones especificas.
		dic = { "on_boton_enviar_clicked" : self.enviar,
		        "on_entry1_activate" : self.enviar,
			"on_entry2_activate" : self.enviar,
			"on_entry3_activate" : self.enviar,
			"on_entry4_activate" : self.enviar,
			"on_entry5_activate" : self.enviar,
			"on_entry6_activate" : self.enviar,
			"on_entry7_activate" : self.enviar,
			"on_entry8_activate" : self.enviar,
			"on_entry9_activate" : self.enviar,
			"on_entry10_activate" : self.enviar,
			"on_entry11_activate" : self.enviar,
			"on_entry12_activate" : self.enviar,
			"on_entry13_activate" : self.enviar,
			"on_entry14_activate" : self.enviar,
			"on_entry15_activate" : self.enviar,
			"on_entry16_activate" : self.enviar,
			"on_text_titulo_activate" : self.enviar,
			"on_text_autor_activate" : self.enviar,			
			"on_text_titulo_activate":self.enviar,
			"on_text_autor_activate":self.enviar,
			"on_boton_cancelar_clicked" : self.cancelar,
			"gtk_main_quit" : gtk.main_quit }
		
		self.widgets.get_widget("ventana_principal").show();
				
		self.widgets.signal_autoconnect(dic)		
		gtk.main()
		
	def cancelar(self, widget):
		print "Que pase Buen Dia!"
                self.widgets.get_widget("ventana_principal").hide();
		exit(0);
				
	def enviar(self, widgets):
		
		info="___________________ NOTA DE USUARIO ___________________\n\n"				
		info+="-\n"			
		texto =self.widgets.get_widget('entry1')	  	
		info+= texto.get_text()
	        info+="-\n"
		texto =self.widgets.get_widget('entry2')	  	
		info+= texto.get_text()
	        info+="-\n"		
		texto =self.widgets.get_widget('entry3')	  	
		info+= texto.get_text()
		info+="-\n"		
		texto =self.widgets.get_widget('entry4')	  	
		info+= texto.get_text()
		info+="-\n"		
		texto =self.widgets.get_widget('entry5')	  	
		info+= texto.get_text()
		info+="-\n"		
		texto =self.widgets.get_widget('entry6')	  	
		info+= texto.get_text()
		info+="-\n"		
		texto =self.widgets.get_widget('entry7')	  	
		info+= texto.get_text()
		info+="-\n"		
		texto =self.widgets.get_widget('entry8')	  	
		info+= texto.get_text()
		info+="-\n"		
		texto =self.widgets.get_widget('entry9')	  	
		info+= texto.get_text()
		info+="-\n"		
		texto =self.widgets.get_widget('entry10')	  	
		info+= texto.get_text()
		info+="-\n"		
		texto =self.widgets.get_widget('entry11')	  	
		info+= texto.get_text()
		info+="-\n"		
		texto =self.widgets.get_widget('entry12')	  	
		info+= texto.get_text()
		info+="-\n"		
		texto =self.widgets.get_widget('entry13')	  	
		info+= texto.get_text()
		info+="-\n"		
		texto =self.widgets.get_widget('entry14')	  	
		info+= texto.get_text()
		info+="-\n"		
		texto =self.widgets.get_widget('entry15')	  	
		info+= texto.get_text()
		info+="-\n"		
		texto =self.widgets.get_widget('entry16')	  	
		info+= texto.get_text()
		#print info		
		info+="-\n"
		if self.widgets.get_widget("pci").get_active() == True:
			info+="----- Dispositivos conectados por PCI:\n"
			info+="-\n"		
			info+=os.popen("lspci").read()
			info+="-\n"
			
		if self.widgets.get_widget("usb").get_active() == True:
			info+="----- Dispositivos conectados por puerto USB:\n\n"
			info+="-\n"
			info+=os.popen("lsusb").read()
			info+="-\n"
			
		if self.widgets.get_widget("t_grafica").get_active() == True:	
			info+="----- Información sobre su tarjeta gráfica:\n\n"
			info+="-\n"
			info+=os.popen("glxinfo").read()
			info+="-\n"
			
		if self.widgets.get_widget("ram").get_active() == True:
			info+="----- Información sobre su memoria RAM (en MB):\n\n"
			info+="-\n"
			info+=os.popen("free -m").read()
			info+="-\n"
			
		if self.widgets.get_widget("d_alma").get_active() == True:
			info+="----- Información sobre su espacio libre :\n\n"
			info+="-\n"
			info+=os.popen("df -h").read()
			info+="-\n"
			
		if self.widgets.get_widget("dd").get_active() == True:
			info+="----- Información sobre sus discos duros :\n\n"
			info+="-\n"
			info+=os.popen("fdisk -l").read()
			
		if self.widgets.get_widget("term").get_active() == True:
			info+="----- Información Archivo term.log :\n\n"
			info+="-\n"
			info+=os.popen("cat /var/log/apt/term.log").read()	
		info+="-\n"
		info+="-*- Información Enviada automáticamente desde el Cliente Notas Canaima:\n\n"
		
		#Titulo de la Nota
		titulo1 = self.widgets.get_widget('text_titulo')
		titulo  = titulo1.get_text()
		autor1 = self.widgets.get_widget('text_autor')
		autor = autor1.get_text()

		params = urllib.urlencode({'codigo_form': info, 'titulo_form': titulo,'nombre_form': autor})
		f = urllib.urlopen("http://notas.canaima.softwarelibre.gob.ve/enviar_consola", params)
		print f.read()
		
		
if __name__ == "__main__":
	correr = nota_canaima()
	gtk.main()
	
		
		


