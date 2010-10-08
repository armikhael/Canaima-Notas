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
		self.vnota=0
		self.vdis=0		
		info="___________________ NOTA DE USUARIO ___________________\n\n"				
		info+="-\n"			
		texto =self.widgets.get_widget('entry1')	
		self.t = texto.get_text()
		info+= texto.get_text()
	        info+="-\n"
		self.vnota=1
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
			self.vdis=1
			
		if self.widgets.get_widget("usb").get_active() == True:
			info+="----- Dispositivos conectados por puerto USB:\n\n"
			info+="-\n"
			info+=os.popen("lsusb").read()
			info+="-\n"
			self.vdis=1
			
		if self.widgets.get_widget("t_grafica").get_active() == True:	
			info+="----- Información sobre su aceleración gráfica:\n\n"
			info+="-\n"
			info+=os.popen("glxinfo").read()
			info+="-\n"
			self.vdis=1
			
		if self.widgets.get_widget("tt_grafica").get_active() == True:	
			info+="----- Información sobre su tarjeta gráfica:\n\n"
			info+="-\n"
			info+=os.popen("hwinfo --framebuffer").read()
			info+="-\n"
			self.vdis=1
			
		if self.widgets.get_widget("ram").get_active() == True:
			info+="----- Información sobre su memoria RAM (en MB):\n\n"
			info+="-\n"
			info+=os.popen("free -m").read()
			info+="-\n"
			self.vdis=1
			
		if self.widgets.get_widget("d_alma").get_active() == True:
			info+="----- Información sobre su espacio libre :\n\n"
			info+="S.ficheros| Tamaño Usado | Disp | Uso% | Montado en\n"
			info+="-\n"
			info+=os.popen("df -h").read()
			info+="-\n"
			self.vdis=1
			
		if self.widgets.get_widget("t_part").get_active() == True:
			info+="----- Información tabla de partición:\n\n"
			info+="-\n"
			info+=os.popen("fdisk -l").read()
			info+="-\n"
			self.vdis=1
		
		if self.widgets.get_widget("cpu").get_active() == True:
			info+="----- Información del procesador:\n\n"
			info+="-\n"
			info+=os.popen("cat /proc/cpuinfo").read()
			info+="-\n"
			self.vdis=1
			
		if self.widgets.get_widget("xorg").get_active() == True:
			info+="----- Información del servidor de pantallas:\n\n"
			info+="-\n"
			info+=os.popen("cat /etc/X11/xorg.conf").read()
			info+="-\n"
			self.vdis=1
			
		if self.widgets.get_widget("repo").get_active() == True:
			info+="----- Información de los repositorios :\n\n"
			info+="-\n"
			info+=os.popen("cat /etc/apt/sources.list").read()	
			info+="-\n"			
			self.vdis=1
			
		if self.widgets.get_widget("modulos").get_active() == True:
			info+="----- Listado de los modulos del kernel:\n\n"
			info+="-\n"
			info+=os.popen("lsmod").read()	
			info+="-\n"			
			self.vdis=1
		
		if self.widgets.get_widget("kernel").get_active() == True:
			info+="----- Kernel del Equipo :\n\n"
			info+="-\n"
			info+=os.popen("uname -a").read()	
			info+="-\n"
			info+="-*- Información Enviada automáticamente desde el Cliente Notas Canaima:\n\n"
			self.vdis=1
			
		#Titulo de la Nota
		titulo1 = self.widgets.get_widget('text_titulo')
		titulo  = titulo1.get_text()		
		autor1 = self.widgets.get_widget('text_autor')
		autor = autor1.get_text()
		
		self.ti = titulo1.get_text()
		self.aut = autor1.get_text()
		
		if (self.t==""):
			md=gtk.MessageDialog(parent=None, flags=0, type=gtk.MESSAGE_QUESTION, buttons=gtk.BUTTONS_CLOSE, message_format="Por Favor!:\nDebes escribir\nen el cuadro de notas")
			md.run()
			md.destroy()
		if (self.vdis==0):			
			md=gtk.MessageDialog(parent=None, flags=0, type=gtk.MESSAGE_QUESTION, buttons=gtk.BUTTONS_CLOSE, message_format="Por Favor!:\nSeleccione al menos una opción a consultar\nen el cuadro de información")
			md.run()
			md.destroy()			
		if (self.ti==""):
			md=gtk.MessageDialog(parent=None, flags=0, type=gtk.MESSAGE_QUESTION, buttons=gtk.BUTTONS_CLOSE, message_format="Es necesario:\nUn título")
			md.run()
			md.destroy()
		if (self.aut==""):
			md=gtk.MessageDialog(parent=None, flags=0, type=gtk.MESSAGE_QUESTION, buttons=gtk.BUTTONS_CLOSE, message_format="Es necesario:\nUn autor")
			md.run()
			md.destroy()
			
		if (self.vdis==0 or self.t=="" or self.ti=="" or self.aut==""):
			md=gtk.MessageDialog(parent=None, flags=0, type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_CLOSE, message_format="No es posible enviar la nota")
			md.run()
			md.destroy()
		else:
			params = urllib.urlencode({'codigo_form': info, 'titulo_form': titulo,'nombre_form': autor})
			f = urllib.urlopen("http://notas.canaima.softwarelibre.gob.ve/enviar_consola", params)
			print f.read()
			md=gtk.MessageDialog(parent=None, flags=0, type=gtk.MESSAGE_INFO, buttons=gtk.BUTTONS_CLOSE, message_format="El envio de la nota a\nhttp://notas.canaima.softwarelibre.gob.ve\nfue exitoso !")
			md.run()
			md.destroy()
		
		
if __name__ == "__main__":
	correr = nota_canaima()
	gtk.main()
	
		
		


