#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
import vte
import webbrowser
import random
import re
import os
import gtk
import sys
import gobject
import threading

gtk.gdk.threads_init()

import time

ita_words2 = ["PONTE", "UFICIO","LINUX","UFICIO","RORAIMA","CUNAGUARO","AREPA","CAYAPAS","OBIWAN","ARRAPC","APONWAO","GNU","FERAL","FJVG","TURPIAL","IDEAS","WARRIOR","HBEARS","REG3X","FRANJ","N3H0","SASHA","thelord","ALGOLIUS"]
ita_words = ["/usr/share/canaima-notas/catpcha/c1.jpg","/usr/share/canaima-notas/catpcha/c2.jpg","/usr/share/canaima-notas/catpcha/c3.jpg","/usr/share/canaima-notas/catpcha/c4.jpg", "/usr/share/canaima-notas/catpcha/c5.jpg", "/usr/share/canaima-notas/catpcha/c18.jpg","/usr/share/canaima-notas/catpcha/c19.jpg", "/usr/share/canaima-notas/catpcha/c20.jpg", "/usr/share/canaima-notas/catpcha/c21.jpg","/usr/share/canaima-notas/catpcha/c22.jpg", "/usr/share/canaima-notas/catpcha/c6.jpg", "/usr/share/canaima-notas/catpcha/c7.jpg","/usr/share/canaima-notas/catpcha/c8.jpg", "/usr/share/canaima-notas/catpcha/c9.jpg", "/usr/share/canaima-notas/catpcha/c10.jpg","/usr/share/canaima-notas/catpcha/c11.jpg", "/usr/share/canaima-notas/catpcha/c12.jpg", "/usr/share/canaima-notas/catpcha/c13.jpg","/usr/share/canaima-notas/catpcha/c14.jpg", "/usr/share/canaima-notas/catpcha/c15.jpg", "/usr/share/canaima-notas/catpcha/c16.jpg", "/usr/share/canaima-notas/catpcha/c17.jpg", "/usr/share/canaima-notas/catpcha/c23.jpg", "/usr/share/canaima-notas/catpcha/c24.jpg"]
posi = ["", ""]


class Main(gtk.Window):
	def __init__(self):
		gtk.Window.__init__(self, gtk.WINDOW_TOPLEVEL)
		gtk.Window.set_position(self, gtk.WIN_POS_CENTER_ALWAYS)
		self.set_title('DOCUMENTADOR DE FALLAS')
		self.set_size_request(600, 520)
		self.set_resizable(False)
		#icono del panel
		self.set_icon_from_file('/usr/share/icons/canaima-iconos/apps/48/tomboy.png')
		self.worker = None
		image = gtk.Image()
		image.set_from_file('/usr/share/canaima-estilo-visual/arte/banner-app-top.png')
		descripcion = gtk.Label()
		descripcion.set_use_markup(True)
		descripcion.set_markup("<span size='small'><b> Bienvenido(a) al documentador de fallas. A través de esta herramienta podrás enviar\n \
texto a la plataforma Canaima, de forma tal que sirva  como  referencia  a  cualquiera\n \
que quiera ayudarte con un tema en particular, incluyendo problemas de hardware y/o\n \
software en  Canaima  GNU/Linux. Opcionalmente  puedes  elegir  varios datos de las\n \
pestañas, por ejemplo la Tarjeta gráfica, Kernel, entre otros.</b></span>")
		#<<<<<<<<<<<<<<<<Sección de Dispositivos>>>>>>>>>>>>>>>>>>>>>>
		self.tabla =  gtk.Table(4,4,True)
		self.check_lspci = gtk.CheckButton("PCI")
		self.check_lspci.set_active(True)
		self.check_lsusb = gtk.CheckButton("USB")
		self.check_lsusb.set_active(False)
		self.check_ram = gtk.CheckButton("RAM/SWAP/Buffers")
		self.check_ram.set_active(False)
		self.check_df = gtk.CheckButton("Espacio Discos")
		self.check_df.set_active(True)
		self.check_cpu = gtk.CheckButton("CPU")
		self.check_cpu.set_active(False)
		self.check_tm = gtk.CheckButton("Tarjeta Madre")
		self.check_tm.set_active(False)
		buttonDIS = self.check_all = gtk.CheckButton("Seleccionar Todos")
		buttonDIS.connect("toggled", self.selectalldis, "Todos")
		self.check_all.set_active(False)
		self.tabla.attach(self.check_lspci,  0, 1, 0, 1)
		self.tabla.attach(self.check_lsusb, 0, 1, 1, 2)
		self.tabla.attach(self.check_ram, 0, 1, 2, 3)
		self.tabla.attach(self.check_df, 1, 2, 0, 1)
		self.tabla.attach(self.check_cpu, 1, 2, 1, 2)
		self.tabla.attach(self.check_tm, 1, 2, 2, 3)
		# Check box para seleccionar todos
		self.tabla.attach(self.check_all, 3, 4, 0, 1)
		self.tabla.show()
		#---------------------------------------------------------------


		#<<<<<<<<<<<<<<<<Sección de informaión del sistema>>>>>>>>>>>>>>>>>>>>>>>>>
		self.tabla1 =  gtk.Table(4,4,True)

		self.check_acelgraf = gtk.CheckButton("Aceleración Gráfica")
		self.check_acelgraf.set_active(False)
		self.check_xorg = gtk.CheckButton("Servidor Pantalla")
		self.check_xorg.set_active(False)
		self.check_repo = gtk.CheckButton("Repositorios")
		self.check_repo.set_active(True)
		self.check_tpart = gtk.CheckButton("Tabla de partición")
		self.check_tpart.set_active(True)
		self.check_prefe = gtk.CheckButton("Prioridad APT")
		self.check_prefe.set_active(False)
		self.check_ired = gtk.CheckButton("Interfaces de RED")
		self.check_ired.set_active(False)
		#self.check_logsys = gtk.CheckButton("LOG del systema")
		#self.check_logsys.set_active(False)

		buttonIsys = self.check_all2 = gtk.CheckButton("Seleccionar Todos")
		buttonIsys.connect("toggled", self.selectalldis2, "Todos")
		self.check_all2.set_active(False)


		self.tabla1.attach(self.check_acelgraf,  0, 1, 0, 1)
		self.tabla1.attach(self.check_xorg, 0, 1, 1, 2)
		self.tabla1.attach(self.check_repo, 0, 1, 2, 3)

		self.tabla1.attach(self.check_tpart, 1, 2, 0, 1)
		self.tabla1.attach(self.check_prefe, 1, 2, 1, 2)
		self.tabla1.attach(self.check_ired, 1, 2, 2, 3)

		#self.tabla1.attach(self.check_logsys, 2, 3, 0, 1)

		# Check box para seleccionar todos
		self.tabla1.attach(self.check_all2, 3, 4, 0, 1)

		self.tabla1.show()

		#<<<<<<<<<<<<<<<<<<Sección de Kernell>>>>>>>>>>>>>>>>>>>>>>>>>>>
		self.tabla2 =  gtk.Table(4,4,True)

		self.check_vers = gtk.CheckButton("Versión")
		self.check_vers.set_active(True)
		self.check_modu = gtk.CheckButton("Modulos")
		self.check_modu.set_active(False)

		buttonK = self.check_all3 = gtk.CheckButton("Seleccionar Todos")
		buttonK.connect("toggled", self.selectalldis3, "Todos")
		self.check_all3.set_active(False)

		self.tabla2.attach(self.check_vers,  0, 1, 0, 1)
		self.tabla2.attach(self.check_modu, 0, 1, 1, 2)

		# Check box para seleccionar todos
		self.tabla2.attach(self.check_all3, 3, 4, 0, 1)

		self.tabla2.show()

		#***********************   NOTEBOOK   **************************

		self.notebook = gtk.Notebook()
		self.notebook.set_tab_pos(gtk.POS_TOP)

		label = gtk.Label("Dispositivos")
		self.notebook.insert_page(self.tabla, label, 1)

		label = gtk.Label("Información del Sistema")
		self.notebook.insert_page(self.tabla1, label, 2)

		label = gtk.Label("Kernel")
		self.notebook.insert_page(self.tabla2, label, 3)
		#---------------------------------------------------------------


		#definimos el scroll
		self.scrolledwindow = gtk.ScrolledWindow()
		self.scrolledwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)

		#Marco del cuadro de notas
		marco = gtk.Frame("Documentar Falla")

		#Marco de los Datos a Enviar
		marco_1 = gtk.Frame("Seleccione Datos a Enviar")
		marco_1.add(self.notebook)
		#Alineacion del cuadro de notas
		self.alineacion = gtk.Alignment(xalign=0.5, yalign=0.3, xscale=0.98, yscale=0.5)

		#text view
		self.textview = gtk.TextView()
		self.textbuffer = self.textview.get_buffer()
		#scroll
		self.scrolledwindow.add(self.textview)
		self.alineacion.add(self.scrolledwindow)
		marco.add(self.alineacion)
		#self.hcaja = gtk.Hbox(False, 0)

		# Creación de etiquetas

		# Creación de barras de progreso
		#self.pbar1 = gtk.ProgressBar()
		#self.pbar2 = gtk.ProgressBar()
		#self.borrar_usuario.set_active(True)

		# Caja titulo autor y captcha

		titulo = gtk.Label("Titulo:")
		autor = gtk.Label("Autor:")
		validador = gtk.Label("        Escribe lo que")
		validador2 = gtk.Label("ves en la imagen")

		captcha = gtk.Image()
		captcha.set_size_request(70,24)
		self.ran_word = random.choice(ita_words)
		self.v = ita_words.index(self.ran_word)
		posi.insert(0, self.v)

		self.d = ita_words2[self.v]
		captcha.set_from_file(self.ran_word)

		self.Titulo = gtk.Entry(15)
		self.Autor = gtk.Entry(15)
		self.Dato = gtk.Entry(15)
		self.i = str(self.v)
		#self.Titulo.set_text(self.i)

		self.tabla_T = gtk.Table(1,5,True)
		self.tabla_T.attach(titulo, 0, 1, 0, 1)
		self.tabla_T.attach(self.Titulo, 1, 2, 0, 1)
		self.tabla_T.attach(autor, 2, 3, 0, 1)
		self.tabla_T.attach(self.Autor, 3, 4, 0, 1)
		self.tabla_T.show()

		self.tabla_V = gtk.Table(1,5,True)
		self.tabla_V.attach(validador, 0, 1, 0, 1)
		self.tabla_V.attach(validador2, 1, 2, 0, 1)
		self.tabla_V.attach(captcha, 2, 3, 0, 1)
		self.tabla_V.attach(self.Dato, 3, 4, 0, 1)
		self.tabla_V.show()

		self.check_gdocum = gtk.CheckButton("Ver Documento (No enviar)")
		self.check_gdocum.set_active(False)

		# Creación de botones
		self.cerrar = gtk.Button(stock=gtk.STOCK_CLOSE)
		self.aceptar = gtk.Button(stock=gtk.STOCK_OK)
		self.ayuda = gtk.Button(stock=gtk.STOCK_HELP)
		button_box = gtk.HButtonBox()
		button_box.set_layout(gtk.BUTTONBOX_SPREAD)
		button_box.pack_start(self.ayuda, False, False)
		button_box.pack_start(self.cerrar, False, False)
		button_box.pack_start(self.aceptar, False, False)

		vbox = gtk.VBox(False, 0)
		vbox.pack_start(image, False, False, 6)
		#vbox.pack_start(titulo, False, False, 0)
		vbox.pack_start(descripcion, False, False, 0)
		vbox.pack_start(marco, False, False, 4)
		vbox.pack_start(marco_1, False, False, 4)
		vbox.pack_start(self.scrolledwindow, True, True, 0)
		vbox.pack_start(self.check_gdocum, False, False, 0)
		#vbox.pack_start(descripcion2, False, False, 0)
		#vbox.pack_start(box, False, False, 0)
		#vbox.pack_start(notebook, False, False, 0)
		vbox.pack_start(self.tabla_T, False, False, 0)
		vbox.pack_start(self.tabla_V, False, False, 0)
		vbox.pack_start(button_box, False, False, 4)

		self.add(vbox)

		self.ayuda.connect("clicked", self.__acerca_de)
		self.cerrar.connect("clicked", self.__close)
		self.aceptar.connect("clicked", self.__validate, posi, captcha, self.textview)

		#vbox.pack_start(scrolledwindow, True, True, 0)
		#scrolledwindow.add(self.textview)

		self.show_all()

	def selectalldis(self, widget, data=None):

		if self.check_all.get_active() == True:

			self.check_lspci.set_active(True)
			self.check_lsusb.set_active(True)
			self.check_ram.set_active(True)
			self.check_df.set_active(True)
			self.check_cpu.set_active(True)
			self.check_tm.set_active(True)
		else:
			self.check_lspci.set_active(False)
			self.check_lsusb.set_active(False)
			self.check_ram.set_active(False)
			self.check_df.set_active(False)
			self.check_cpu.set_active(False)
			self.check_tm.set_active(False)

	def selectalldis2(self, widget, data=None):

		if self.check_all2.get_active() == True:

			self.check_acelgraf.set_active(True)
			self.check_xorg.set_active(True)
			self.check_repo.set_active(True)
			self.check_tpart.set_active(True)
			self.check_prefe.set_active(True)
			self.check_ired.set_active(True)
			self.check_logsys.set_active(True)

		else:
			self.check_acelgraf.set_active(False)
			self.check_xorg.set_active(False)
			self.check_repo.set_active(False)
			self.check_tpart.set_active(False)
			self.check_prefe.set_active(False)
			self.check_ired.set_active(False)
			self.check_logsys.set_active(False)

	def selectalldis3(self, widget, data=None):

		if self.check_all3.get_active() == True:

			self.check_vers.set_active(True)
			self.check_modu.set_active(True)

		else:
			self.check_vers.set_active(False)
			self.check_modu.set_active(False)

	def __acerca_de(self, widget):
		about = gtk.AboutDialog()
		about.set_type_hint(gtk.gdk.WINDOW_TYPE_HINT_DIALOG)
		about.set_logo(gtk.gdk.pixbuf_new_from_file('/usr/share/icons/canaima-iconos/apps/48/tomboy.png'))#canaima.png
		about.set_name('Documentador de Fallas')
		about.set_comments("CLIENTE DE LA PLATAFORMA DE NOTAS\
\n\n  Permite Documentar las fallas del sistema, utilizando comandos especializados de GNU/linux. \
El usuario en el cuadro 'Documentar Falla' podrá escribir su percepción del problema. \
El cuadro 'Seleccione datos a enviar' son una serie de comandos predefinidos, que diagnosticaran el sistema dependiendo \
 de la categoría en que se encuentre como 'Dispositivos', 'Información de sistema' o 'Kernel'. \n\nLuego \
el botón ACEPTAR, envía todos estos datos a la plataforma de 'http://notas.canaima.softwarelibre.gob.ve/' o si lo desea podrá ver el documento que el sistema genera.\n\
Seleccionando la opción de 'Ver documento'\n\n Nota: toda la información proporcionada es utilizada por los técnicos de la comunidad Canaima \
para solucionar el problema de su sistema. \
")
		about.set_transient_for(self)
		about.set_position(gtk.WIN_POS_CENTER_ON_PARENT)

		authors = []
		try:
			f = file('AUTHORS', 'r')
			for line in f:
				authors.append(line.strip('\n'))
			f.close()
		except Exception, msg:
			authors = [_("File 'AUTHORS' not found")]
		about.set_authors(authors)
		about.connect("response", self.__about_response)
		about.connect("close", self.__about_close)
		about.connect("delete_event", self.__about_close)
		about.run()

	def __about_response(self, dialog, response, *args):
		if response < 0:
			dialog.destroy()
			dialog.emit_stop_by_name('response')

	def __about_close(self, widget, event=None):
		widget.destroy()
		return True

	def __reset(self, user=True, root=True):
		if user:
			self.user_passwd1.set_text('')
			self.user_passwd2.set_text('')
		if root:
			self.admin_passwd1.set_text('')
			self.admin_passwd2.set_text('')

	def __validate(self, widget, posi, captcha, textview):


		h = posi.pop(0)
		h2 = int(h)
		self.d = ita_words2[h2]

		#validacion del captcha
		if  self.Dato.get_text() != self.d or self.Dato.get_text() == '':

			md=gtk.MessageDialog(parent=None, flags=0, type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_CLOSE, message_format="El valor introducido no coincide con el captcha intente de nuevo")
			md.run()
			md.destroy()

			captcha.clear()
			captcha.set_size_request(70,24)
			self.ran_word = random.choice(ita_words)
			self.v = ita_words.index(self.ran_word)
			posi.insert(0, self.v)
			captcha.set_from_file(self.ran_word)
			self.tabla_V.attach(captcha, 2, 3, 0, 1)

		else:

			self.vdis=0
			info="\n___________________ NOTA DE USUARIO ___________________\n\n"
			info+="-\n"

			self.textbuffer = textview.get_buffer()
			start, end = self.textbuffer.get_bounds()
			self.dnota = self.textbuffer.get_text(start,end)

			#--------------------capchat---------------------------
			captcha.clear()
			captcha.set_size_request(70,24)
			self.ran_word = random.choice(ita_words)
			self.v = ita_words.index(self.ran_word)
			posi.insert(0, self.v)
			captcha.set_from_file(self.ran_word)
			self.tabla_V.attach(captcha, 2, 3, 0, 1)
			#--------------------capchat---------------------------

			#Titulo de la Nota
			titulo  = self.Titulo.get_text()
			autor = self.Autor.get_text()


			info+= self.textbuffer.get_text(start,end)
			info+="-\n"
			if self.check_lspci.get_active() == True:
				info+="----- Dispositivos conectados por PCI:\n"
				info+="-\n"
				info+=os.popen("lspci").read()
				info+="-\n"
				self.vdis=1

			if self.check_tm.get_active() == True:
				info+="----- Tarjeta Madre -----:\n"
				info+="-\n"
				info+=os.popen("lspci | grep 'Host bridge:'").read()
				info+="-\n"
				self.vdis=1

			if self.check_lsusb.get_active() == True:
				info+="----- Dispositivos conectados por puerto USB:\n\n"
				info+="-\n"
				info+=os.popen("lsusb").read()
				info+="-\n"
				self.vdis=1

			if self.check_acelgraf.get_active() == True:
				info+="----- Información sobre su aceleración gráfica:\n\n"
				info+="-\n"
				info+=os.popen("glxinfo | grep -A4 'name of display:'").read()
				info+="-\n"
				self.vdis=1

			if self.check_ired.get_active() == True:
				info+="----- Información interfaces de RED:\n\n"
				info+="-\n"
				info+=os.popen("cat /etc/network/interfaces").read()
				info+="-\n"
				self.vdis=1

			if self.check_prefe.get_active() == True:
				info+="----- Información /etc/apt/preferences:\n\n"
				info+="-\n"
				info+=os.popen("cat /etc/apt/preferences").read()
				info+="-\n"
				self.vdis=1

			if self.check_ram.get_active() == True:
				info+="----- Información sobre su memoria RAM, Swap, y Buffer (en MB):\n\n"
				info+="-\n"
				info+=os.popen("free -m").read()
				info+="-\n"
				self.vdis=1

			if self.check_df.get_active() == True:
				info+="----- Espacio libre en los dispositivos de almacenamiento :\n\n"
				info+="S.ficheros| Tamaño Usado | Disp | Uso% | Montado en\n"
				info+="-\n"
				info+=os.popen("df -h").read()
				info+="-\n"
				self.vdis=1

			if self.check_tpart.get_active() == True:
				info+="----- Información tabla de partición:\n\n"
				info+="-\n"
				info+=os.popen("fdisk -l").read()
				info+="-\n"
				self.vdis=1

			if self.check_cpu.get_active() == True:
				info+="----- Información del procesador:\n\n"
				info+="-\n"
				info+=os.popen("cat /proc/cpuinfo").read()
				info+="-\n"
				self.vdis=1

			#if self.check_logsys.get_active() == True:
			#	info+="----- Log del Systema:----------\n\n"
			#	info+="-\n"
			#	info+=os.popen("gksu cat /var/log/syslog|grep 'error'").read()
			#	info+="-\n"
			#	self.vdis=1

			if self.check_xorg.get_active() == True:
				info+="----- Información del servidor de pantallas en Canaima 2.1 (lenny):\n\n"
				info+="-\n"
				info+=os.popen("cat /etc/X11/xorg.conf").read()
				info+="-\n"
				info+="----- Información  log error de xorg en Canaima 3.0 (squeeze):\n\n"
				info+="-\n"
				info+=os.popen("cat /var/log/Xorg.0.log | grep 'error'").read()
				info+="-\n"
				self.vdis=1

			if self.check_repo.get_active() == True:
				info+="----- Información de los repositorios :\n\n"
				info+="-\n"
				info+=os.popen("cat /etc/apt/sources.list").read()
				info+="-\n"
				self.vdis=1

			if self.check_modu.get_active() == True:
				info+="----- Listado de los modulos del kernel:\n\n"
				info+="-\n"
				info+=os.popen("lsmod").read()
				info+="-\n"
				self.vdis=1

			if self.check_vers.get_active() == True:
				info+="-----Versión del Kernel :\n\n"
				info+="-\n"
				info+=os.popen("uname -a").read()
				info+="-\n"
				info+="-*- Información Enviada automáticamente desde el Documentador de Fallas (Cliente Notas Canaima):\n\n"
				self.vdis=1


			if self.dnota == "":
				md=gtk.MessageDialog(parent=None, flags=0, type=gtk.MESSAGE_QUESTION, buttons=gtk.BUTTONS_CLOSE, message_format="Por Favor!:\nTomese unos instantes y describa su situación o inconveniente\n en el Cuadro de Documentar Falla")
				md.run()
				md.destroy()
				#self.__close2()
			if (self.vdis==0):
				md=gtk.MessageDialog(parent=None, flags=0, type=gtk.MESSAGE_QUESTION, buttons=gtk.BUTTONS_CLOSE, message_format="Por Favor!:\nSeleccione al menos una opción a consultar\ndel cuadro Seleccione datos a enviar")
				md.run()
				md.destroy()
			if (self.Titulo.get_text()==""):
				md=gtk.MessageDialog(parent=None, flags=0, type=gtk.MESSAGE_QUESTION, buttons=gtk.BUTTONS_CLOSE, message_format="Es necesario:\nUn título")
				md.run()
				md.destroy()
			if (self.Autor.get_text()==""):
				md=gtk.MessageDialog(parent=None, flags=0, type=gtk.MESSAGE_QUESTION, buttons=gtk.BUTTONS_CLOSE, message_format="Es necesario:\nUn autor")
				md.run()
				md.destroy()

			if (self.dnota == "" or self.vdis==0 or self.Titulo.get_text()=="" or self.Autor.get_text()==""):
				md=gtk.MessageDialog(parent=None, flags=0, type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_CLOSE, message_format="No es posible enviar la nota o ver el informe")
				md.run()
				md.destroy()

			else:

				if self.check_gdocum.get_active() == True:
					filedf = open('/tmp/Documento.txt','w')
					filedf.writelines(titulo)
					filedf.writelines(autor)
					filedf.writelines(info)
					filedf.close()
					os.popen("gedit /tmp/Documento.txt")
				else:
					params = urllib.urlencode({'codigo_form': info, 'titulo_form': titulo,'nombre_form': autor})
					f = urllib.urlopen("http://notas.canaima.softwarelibre.gob.ve/enviar_consola", params)
					#print f.read()
					self.mes = f.read()
					md=gtk.MessageDialog(parent=None, flags=0, type=gtk.MESSAGE_INFO, buttons=gtk.BUTTONS_CLOSE, message_format= "El envio de la nota fue exitoso..!\n "+str(self.mes))
					md.run()
					md.destroy()

		self.aceptar.set_sensitive(True)
		self.cerrar.set_sensitive(True)

	#def __close2(self, widget=None):
		#self.destroy()


	def __close(self, widget=None):
		self.destroy()
		gtk.main_quit()
		sys.exit(0)


if __name__=="__main__":
	base = Main()
	gtk.main()
