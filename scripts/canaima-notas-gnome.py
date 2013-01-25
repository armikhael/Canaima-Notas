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
from threading import Thread

from subprocess import Popen, PIPE, STDOUT

#import random
import Image
import ImageFont
import ImageDraw
import ImageFilter

gtk.gdk.threads_init()

import time

#----------------------------Ayuda-----------------------
def clic_ayuda(self):
	hilo = threading.Thread(target=ayuda_1, args=(self))
	hilo.start()
		
def ayuda_1(self, widget=None):			
	x= Popen(["yelp /usr/share/gnome/help/canaima-notas-gnome/es/c-n.xml"], shell=True, stdout=PIPE)
#-------------------------------------------------------

#--------------------------imagen construir---------------------------------------
def gen_random_word(wordLen=6):
    allowedChars = "abcdefghijklmnopqrstuvwzyzABCDEFGHIJKLMNOPQRSTUVWZYZ0123456789"
    word = ""
    for i in range(0, wordLen):
        word = word + allowedChars[random.randint(0,0xffffff) % len(allowedChars)]
    return word
    
def gen_captcha(text, fnt, fnt_sz, file_name, fmt='JPEG'):      
    fgcolor = random.randint(0,1)
    bgcolor = fgcolor ^ 0xffffff
    font = ImageFont.truetype(fnt,fnt_sz)
    dim = font.getsize(text)
    im = Image.new('RGB', (dim[0]+5,dim[1]+5), bgcolor)
    d = ImageDraw.Draw(im)
    x, y = im.size
    r = random.randint
    for num in range(100):
        d.rectangle((r(0,x),r(0,y),r(0,x),r(0,y)),fill=r(0,0xffffff))
    d.text((3,3), text, font=font, fill=fgcolor)
    im = im.filter(ImageFilter.EDGE_ENHANCE_MORE)
    im.save(file_name, format=fmt)
#-------------------------------------------------------------------------------
#---------------------threading para la variable systema------------------------
class TestThread(threading.Thread):
    def __init__(self, mainview):
        threading.Thread.__init__(self)

    def run(self):
        systema= os.system("gedit /tmp/Documento.txt")
#--------------------------------------------------------------------------------
class TestThread2(threading.Thread):
    def __init__(self, mainview):
        threading.Thread.__init__(self)

    def run(self):
        systema= os.system("sensible-browser http://notas.canaima.softwarelibre.gob.ve/")

class Main(gtk.Window):
	
	def __init__(self):
		self.word = gen_random_word()
		gen_captcha(self.word.strip(), '/usr/share/fonts/truetype/ttf-dejavu/DejaVuSans.ttf', 20, '/tmp/test.jpg')
		
		gtk.Window.__init__(self, gtk.WINDOW_TOPLEVEL)
		gtk.Window.set_position(self, gtk.WIN_POS_CENTER_ALWAYS)
		self.worker = None
		self.set_title('Documentador de Fallas')
		self.connect("delete_event",self.on_delete)

		# Banner del panel
		self.set_resizable(False)
		if os.path.isfile('../img/banner-app-top.png'):
                	self.set_size_request(600, 520)
		else:
			self.set_size_request(600, 440)
		if os.path.basename('../img/banner-app-top.png') == 'banner-app-top.png':
			image = gtk.Image()
			image.set_from_file('../img/banner-app-top.png')

		#Icono del panel
		self.set_icon_from_file('../img/canaima-notas-icons.png')
		
		#--------------------------------Primera caja--------------------------------------------
		self.descripcion = gtk.Label()
		self.descripcion.set_markup("<b> Bienvenido al Documentador de Fallas</b>")
		#-------------------------Separadores
		self.separator1 = gtk.HSeparator()
		self.separator2 = gtk.HSeparator()
		self.separator3 = gtk.HSeparator()
		
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
		self.flags_buffer = True
		self.textview = gtk.TextView()
		self.textbuffer = self.textview.get_buffer()
		self.textview.set_editable(True)
		self.textbuffer.set_text("\n\n\t\t\t\tEscriba el problema que ocurrió en su computador")
		self.textview.connect('event', self.on_entry_buffer_clicked)
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
		#------------------------------------------------------------------------
		titulo = gtk.Label("Titulo:")
		autor = gtk.Label("Autor:")
		validador = gtk.Label("        Escribe lo que")
		validador2 = gtk.Label("ves en la imagen")

		self.captcha_ima = gtk.Image()
		self.captcha_ima.set_from_file('/tmp/test.jpg')
		#self.captcha_ima.connect('clicked', self.refresh_captcha)
		
		#############################################################################################################################------------
	
		self.Titulo = gtk.Entry(20)
		self.Autor = gtk.Entry(30)
		self.Dato = gtk.Entry(6)
		
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
		self.tabla_V.attach(self.captcha_ima, 2, 3, 0, 1)################################################################################33
		self.tabla_V.attach(self.Dato, 3, 4, 0, 1)
		self.tabla_V.show()

		self.check_gdocum = gtk.CheckButton("Ver Documento (No enviar)")
		self.check_gdocum.set_active(False)

		# Creación de botones--------------------------caja botones----------------------------
		self.cerrar = gtk.Button(stock=gtk.STOCK_CLOSE)
		self.cerrar.set_size_request(80, 30)
		self.aceptar = gtk.Button(stock=gtk.STOCK_OK)
		self.aceptar.set_size_request(80, 30)
		self.ayuda = gtk.Button(stock=gtk.STOCK_HELP)
		self.ayuda.set_size_request(80, 30)
		#button_box = gtk.HButtonBox()
		button_box= gtk.HBox(False, False)
		#button_box.set_layout(gtk.BUTTONBOX_SPREAD)
		button_box.pack_start(self.cerrar, False, False,10)
		button_box.pack_start(self.ayuda, False, False,5)
		button_box.pack_start(self.aceptar, False, False,315)

		#-------------------------------------caja entry de correo---------------------------
		self.correo = gtk.Label()
		self.correo.set_markup("Email:")
		
		self.flags_correo = True
		self.entry_correo = gtk.Entry()
		self.entry_correo.set_editable(True)
		self.entry_correo.set_text("correo@ejemplo.com")
		self.entry_correo.connect('event', self.on_entry_correo_clicked)
		
		self.label_1 = gtk.Label()
		self.label_1.set_markup("")
		
		caja_correo= gtk.HBox(False, False)
		caja_correo.pack_start(self.correo, False, False,40)
		caja_correo.pack_start(self.entry_correo, True, True,0)
		caja_correo.pack_start(self.label_1, False, False,60)

		#----------------------------------------------------------------------------------------
		
		
		#-----------------------------------CAJA DE WINDOW-------------------------------------
		vbox = gtk.VBox(False, 0)
		marco.set_border_width(2)
		marco_1.set_border_width(2)

		if os.path.isfile('../img/banner-app-top.png'):
			vbox.pack_start(image, False, False, 3)
		
		vbox.add(self.separator2)
		vbox.add(self.tabla_T)
		vbox.add(caja_correo)
		vbox.add(marco)
		vbox.add(marco_1)
		#vbox.pack_start(self.scrolledwindow, True, True, 0)#----------------------error---------------------------------
		vbox.add(self.check_gdocum)	
		vbox.add(self.tabla_V)
		vbox.add(self.separator3)
		#vbox.add(button_box)
		vbox.pack_start(button_box, False, False, 0)
		
		self.add(vbox)
		#-------------------------------------------------------------------------------
		
		#----------------------conectar botones a las funciones------------------
		self.ayuda.connect("clicked", clic_ayuda)
		self.cerrar.connect("clicked", self.__close)
		self.aceptar.connect("clicked", self.__validate, self.textview)
		#---------------------------------------------------------------------------
		
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

	def __validate(self, widget, textview):

		if self.Titulo.get_text():
			
			if self.Autor.get_text():
				
				if re.match('^[(a-z0-9\_\-\.)]+@[(a-z0-9\_\-\.)]+\.[(a-z)]{2,4}$',self.entry_correo.get_text().lower()):
					
					self.textbuffer = textview.get_buffer()
					start, end = self.textbuffer.get_bounds()
					self.dnota = self.textbuffer.get_text(start,end)
					
					if self.dnota:
				
						#validacion del captcha
						if  self.Dato.get_text() != self.word:

							md=gtk.MessageDialog(parent=None, flags=0, type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_CLOSE, message_format="El valor introducido no coincide con el captcha intente de nuevo")
							md.run()
							md.destroy()
							self.refresh_captcha()
							self.Dato.set_text("")													
																				
						else:
							self.refresh_captcha()
							self.vdis=0
							info= "DIRECCIÓN DE CORREO ELECTRÓNICO: "+ self.entry_correo.get_text()+"\n\n"
							info+="-"
							info+="\n___________________ NOTA DE USUARIO ___________________\n\n"
							info+="-\n"
							
							#--------------------capchat---------------------------
							
							#--------------------capchat---------------------------

							#Titulo de la Nota
							titulo_1  = self.Titulo.get_text()
							autor_1 = self.Autor.get_text()
							
							titulo_2  = "TITULO: "+self.Titulo.get_text()+"\n\n"
							autor_2 = "AUTOR: "+self.Autor.get_text()+"\n\n"


							info+= self.textbuffer.get_text(start,end)
							info+="\n"
							if self.check_lspci.get_active() == True:
								info+="-\n"
								info+="__________________________________________________________"
								info+="\n\n----- Dispositivos conectados por PCI:\n"
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
							
							if (self.vdis==0):
								md=gtk.MessageDialog(parent=None, flags=0, type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_CLOSE, message_format="Por Favor!:\nSeleccione al menos una opción a consultar\ndel cuadro Seleccione datos a enviar.")
								md.run()
								md.destroy()		

							if (self.dnota == "" or self.vdis==0 or self.Titulo.get_text()=="" or self.Autor.get_text()==""):
								md=gtk.MessageDialog(parent=None, flags=0, type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_CLOSE, message_format="No es posible enviar la nota o ver el informe.")
								md.run()
								md.destroy()

							else:

								if self.check_gdocum.get_active() == True:
									filedf = open('/tmp/Documento.txt','w')
									filedf.writelines(titulo_2)
									filedf.writelines(autor_2)
									filedf.writelines(info)
									filedf.close()									
									worker = TestThread(self)
									worker.start()
									#os.popen("gedit /tmp/Documento.txt")
																										
								else:
									
									def prueba_inter(self):
										pru = os.system("wget -P /tmp http://www.google.co.ve/")
										t = next(os.walk('/tmp/'))[2]
										a = 'index.html'
										b = ''
										for b in t:
											if b == a:					
												borrar = os.system('rm /tmp/index.html')
												return True
											else:
												pass
					
									if prueba_inter(self) == True:
									
										params = urllib.urlencode({'codigo_form': info, 'titulo_form': titulo_1,'nombre_form': autor_1})
										f = urllib.urlopen("http://notas.canaima.softwarelibre.gob.ve/enviar_consola", params)									
										self.mes = f.read()
										#print self.mes
										md=gtk.MessageDialog(parent=None, flags=0, type=gtk.MESSAGE_INFO, buttons=gtk.BUTTONS_CLOSE, message_format= "El envio de la nota fue exitoso...!\n "+str(self.mes))
										md.run()
										md.destroy()
										worker = TestThread2(self)
										worker.start()
										#systema= os.system("cunaguaro http://notas.canaima.softwarelibre.gob.ve/")
										
									else:
										
										md=gtk.MessageDialog(parent=None, flags=0, type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_CLOSE, message_format="\tEl reporte no podrá ser enviado a la plataforma de \t\n\tCanaima, porque no posee una conexión a internet.\n\n\tPero puedo verlo en el sistema con la opción \n\tVer Documento (No Enviar).")
										md.set_title('Error en Conexión')
										md.run()
										md.destroy()
										self.check_gdocum.set_active(True)
												
					else:
						md=gtk.MessageDialog(parent=None, flags=0, type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_CLOSE, message_format="Por Favor!:\nTomese unos instantes y describa su situación o inconveniente\n en el Cuadro de Documentar Falla.")
						md.run()
						md.destroy()
						self.refresh_captcha()
						
				else:
					md=gtk.MessageDialog(parent=None, flags=0, type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_CLOSE, message_format="Es necesario que coloque una Dirección de correo electrónico.\n\n\t\t Ejemplo : correo@ejemplo.com")
					md.run()
					md.destroy()
					self.refresh_captcha()			
			else:
				md=gtk.MessageDialog(parent=None, flags=0, type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_CLOSE, message_format="Es necesario que coloque un Autor.")
				md.run()
				md.destroy()
				self.refresh_captcha()
					
		else:		
			md=gtk.MessageDialog(parent=None, flags=0, type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_CLOSE, message_format="Es necesario que coloque un título.")
			md.run()
			md.destroy()
			self.refresh_captcha()
	
		#self.aceptar.set_sensitive(True)
		#self.cerrar.set_sensitive(True)

	#def __close2(self, widget=None):
		#self.destroy()
	def refresh_captcha(self):
		self.word = gen_random_word()
		gen_captcha(self.word.strip(), '/usr/share/fonts/truetype/ttf-dejavu/DejaVuSans.ttf', 20, '/tmp/test.jpg')		
		self.captcha_ima.set_from_file('/tmp/test.jpg')

	def __close(self, widget=None):
		if self.Titulo.get_text() or self.Autor.get_text():
			md=gtk.MessageDialog(parent=None, flags=0, type=gtk.MESSAGE_QUESTION, buttons=gtk.BUTTONS_YES_NO, message_format="Al cerrar, todos los procedimientos que este generando el Documentador de Fallas serán cerrados.\n\n\t¿Desea salir de la aplicación?")
			md.set_title('Cerrar')
			respuesta = md.run()
			md.destroy()
		
			if respuesta == gtk.RESPONSE_YES:
				systema= os.system("rm /tmp/test.jpg")
				self.destroy()
				gtk.main_quit()
			
		else:
			systema= os.system("rm /tmp/test.jpg")
			self.destroy()
			gtk.main_quit()
			#sys.exit(0)
	
	def on_entry_correo_clicked(self, widget, event, data=None):	
		if (self.flags_correo):
			if event.type == gtk.gdk.BUTTON_RELEASE:
				self.entry_correo.set_text("")
				self.flags_correo = False
	
	def on_entry_buffer_clicked(self, widget, event, data=None):	
		if (self.flags_buffer):
			if event.type == gtk.gdk.BUTTON_RELEASE:
				self.textbuffer.set_text("")
				self.flags_buffer = False
	
	def close(self):
		md=gtk.MessageDialog(parent=None, flags=0, type=gtk.MESSAGE_QUESTION, buttons=gtk.BUTTONS_YES_NO, message_format="Al cerrar, todos los procedimientos que este generando el Documentador de Fallas serán cerrados.\n\n\t¿Desea salir de la aplicación?")
		md.set_title('Cerrar')
		respuesta = md.run()
		md.destroy()
		
		if respuesta == gtk.RESPONSE_YES:
			systema= os.system("rm /tmp/test.jpg")
			self.destroy()
			gtk.main_quit()
	
	def on_delete(self, widget, data=None):
		return not self.close()


if __name__=="__main__":
	base = Main()
	gtk.main()
