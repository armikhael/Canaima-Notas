#!/usr/bin/env python
# -*- coding: utf-8 -*-
#==============================================================================
#
# Copyright (C) 2010 Canaima GNU/Linux
# <desarrolladores@canaima.softwarelibre.gob.ve>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
#
#==============================================================================

from common import ICON_PATH, TOP_BANNER_PATH, get_random_word, FONT_CAPTCHA, \
    IMG_CAPTCHA, create_captcha_img, TXT_FILE, URL_PASTE_PLATFORM, \
    launch_help, message_question
import gtk
import os
import re
import threading
import urllib
from validations import is_empty_string, is_valid_email
from note import Note

gtk.gdk.threads_init()

# Clase principal -------------------------------------------------------------


class Main(gtk.Window):

    def __init__(self):

        self.worker = None
        self.flags_correo = True
        self.flags_buffer = True

        gtk.Window.__init__(self, gtk.WINDOW_TOPLEVEL)
        gtk.Window.set_position(self, gtk.WIN_POS_CENTER_ALWAYS)
        self.set_resizable(False)
        self.set_title('Documentador de Fallas')
        self.connect("delete_event", self.on_delete)
        # Icono de la ventana
        if os.path.isfile(ICON_PATH):
            self.set_icon_from_file(ICON_PATH)

        # Banner superior >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

        if os.path.isfile(TOP_BANNER_PATH):
            self.img_top_banner = gtk.Image()
            self.img_top_banner.set_from_file(TOP_BANNER_PATH)
            size = self.img_top_banner.size_request()
            self.set_size_request(size[0], -1)  # -1 porque no importa el alto

        # Identificación >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

        self.lbl_titulo = gtk.Label("Titulo:")
        self.lbl_autor = gtk.Label("Autor:")
        self.lbl_correo = gtk.Label("Email:")

        self.txt_titulo = gtk.Entry(20)
        self.txt_autor = gtk.Entry(30)
        self.txt_correo = gtk.Entry()
        self.txt_correo.set_text("correo@ejemplo.com")
        self.txt_correo.connect('event', self.on_txt_correo_clicked)

        self.tbl_indetif = gtk.Table(2, 6, True)
        self.tbl_indetif.attach(self.lbl_titulo, 0, 1, 0, 1)
        self.tbl_indetif.attach(self.txt_titulo, 1, 5, 0, 1)

        self.tbl_indetif.attach(self.lbl_autor, 0, 1, 1, 2)
        self.tbl_indetif.attach(self.txt_autor, 1, 2, 1, 2)
        self.tbl_indetif.attach(self.lbl_correo, 2, 3, 1, 2)
        self.tbl_indetif.attach(self.txt_correo, 3, 5, 1, 2)

        self.tbl_indetif.show()

        # Descripcion de la falla >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

        self.textview = gtk.TextView()
        self.textbuffer = self.textview.get_buffer()
        self.textview.set_editable(True)
        self.textbuffer.set_text("\n\n\t\t\t\tEscriba el problema que ocurrió \
en su computador")
        self.textview.connect('event', self.on_entry_buffer_clicked)

        self.scrolledwindow = gtk.ScrolledWindow()
        self.scrolledwindow.set_policy(gtk.POLICY_AUTOMATIC, \
                                       gtk.POLICY_AUTOMATIC)
        self.scrolledwindow.add(self.textview)

        self.alineacion = gtk.Alignment(xalign=0.5, yalign=0.3, xscale=0.98, \
                                        yscale=0.5)
        self.alineacion.add(self.scrolledwindow)

        marco = gtk.Frame("Escriba los detalles de la falla (sea lo más \
específico posible):")
        marco.set_border_width(2)
        marco.add(self.alineacion)

        # Pestañas >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

        # Sección de dispositivos
        self.tabla = gtk.Table(4, 4, True)

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
        self.check_all = gtk.CheckButton("Seleccionar Todos")
        self.check_all.connect("toggled", self.selectalldis, "Todos")

        self.check_all.set_active(False)
        self.tabla.attach(self.check_lspci, 0, 1, 0, 1)
        self.tabla.attach(self.check_lsusb, 0, 1, 1, 2)
        self.tabla.attach(self.check_ram, 0, 1, 2, 3)
        self.tabla.attach(self.check_df, 1, 2, 0, 1)
        self.tabla.attach(self.check_cpu, 1, 2, 1, 2)
        self.tabla.attach(self.check_tm, 1, 2, 2, 3)
        self.tabla.attach(self.check_all, 3, 4, 0, 1)
        self.tabla.show()

        # Seccion de informaión del sistema
        self.tabla1 = gtk.Table(4, 4, True)

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
        self.check_all2 = gtk.CheckButton("Seleccionar Todos")
        self.check_all2.connect("toggled", self.selectalldis2, "Todos")
        self.check_all2.set_active(False)

        self.tabla1.attach(self.check_acelgraf, 0, 1, 0, 1)
        self.tabla1.attach(self.check_xorg, 0, 1, 1, 2)
        self.tabla1.attach(self.check_repo, 0, 1, 2, 3)
        self.tabla1.attach(self.check_tpart, 1, 2, 0, 1)
        self.tabla1.attach(self.check_prefe, 1, 2, 1, 2)
        self.tabla1.attach(self.check_ired, 1, 2, 2, 3)
        self.tabla1.attach(self.check_all2, 3, 4, 0, 1)
        self.tabla1.show()

        # Sección del Kernel
        self.tabla2 = gtk.Table(4, 4, True)

        self.check_vers = gtk.CheckButton("Versión")
        self.check_vers.set_active(True)
        self.check_modu = gtk.CheckButton("Módulos")
        self.check_modu.set_active(False)
        self.check_all3 = gtk.CheckButton("Seleccionar Todos")
        self.check_all3.connect("toggled", self.selectalldis3, "Todos")
        self.check_all3.set_active(False)

        self.tabla2.attach(self.check_vers, 0, 1, 0, 1)
        self.tabla2.attach(self.check_modu, 0, 1, 1, 2)
        self.tabla2.attach(self.check_all3, 3, 4, 0, 1)
        self.tabla2.show()

        self.notebook = gtk.Notebook()
        self.notebook.set_tab_pos(gtk.POS_TOP)
        label = gtk.Label("Dispositivos")
        self.notebook.insert_page(self.tabla, label, 1)
        label = gtk.Label("Información del Sistema")
        self.notebook.insert_page(self.tabla1, label, 2)
        label = gtk.Label("Kernel")
        self.notebook.insert_page(self.tabla2, label, 3)

        marco_1 = gtk.Frame("Seleccione los datos a enviar:")
        marco_1.set_border_width(2)
        marco_1.add(self.notebook)

        # Envío >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

        self.check_gdocum = gtk.CheckButton("Ver Documento (No enviar).")
        self.check_gdocum.set_active(False)

        # Capcha
        lbl_captcha = gtk.Label("Escribe lo que ves en la imagen:")
        lbl_captcha.set_justify(gtk.JUSTIFY_LEFT)
        self.word = get_random_word()
        create_captcha_img(self.word.strip(), FONT_CAPTCHA, 20, IMG_CAPTCHA)
        self.img_captcha = gtk.Image()
        self.img_captcha.set_from_file(IMG_CAPTCHA)
        self.txt_captcha = gtk.Entry(6)

        self.tbl_envio = gtk.Table(2, 5, True)
        self.tbl_envio.attach(self.check_gdocum, 0, 5, 0, 1)
        self.tbl_envio.attach(lbl_captcha, 0, 2, 1, 2)
        self.tbl_envio.attach(self.img_captcha, 2, 3, 1, 2)
        self.tbl_envio.attach(self.txt_captcha, 3, 4, 1, 2)
        self.tbl_envio.show()

        # Caja botones >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

        self.btn_cerrar = gtk.Button(stock=gtk.STOCK_CLOSE)
        self.btn_cerrar.connect("clicked", self.__close)
        self.btn_ayuda = gtk.Button(stock=gtk.STOCK_HELP)
        self.btn_ayuda.connect("clicked", self.on_btn_ayuda_clicked)
        self.btn_aceptar = gtk.Button(stock=gtk.STOCK_OK)
        self.btn_aceptar.connect("clicked", self.__validate, self.textview)

        button_box = gtk.HBox(False, False)
        button_box.pack_start(self.btn_cerrar, False, False, 10)
        button_box.pack_start(self.btn_ayuda, False, False, 5)
        button_box.pack_start(self.btn_aceptar, False, False, 315)

        #----------------------------------------------------------------------

        # Ensamblaje de la ventana
        vbox = gtk.VBox(False, 0)

        if os.path.isfile(TOP_BANNER_PATH):
            vbox.add(self.img_top_banner)

        # Separadores
        self.separator1 = gtk.HSeparator()
        self.separator2 = gtk.HSeparator()

        vbox.add(self.separator1)
        vbox.add(self.tbl_indetif)
        vbox.add(marco)
        vbox.add(marco_1)
        vbox.add(self.tbl_envio)
        vbox.add(self.separator2)
        vbox.pack_start(button_box, False, False, 0)

        self.add(vbox)
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

    # Eventos -----------------------------------------------------------------

    def on_btn_ayuda_clicked(self):
        hilo = threading.Thread(target=launch_help, args=(self))
        hilo.start()

    def on_txt_correo_clicked(self, widget, event, data=None):
        if (self.flags_correo):
            if event.type == gtk.gdk.BUTTON_RELEASE:
                self.txt_correo.set_text("")
                self.flags_correo = False

    def on_entry_buffer_clicked(self, widget, event, data=None):
        if (self.flags_buffer):
            if event.type == gtk.gdk.BUTTON_RELEASE:
                self.textbuffer.set_text("")
                self.flags_buffer = False

    def on_delete(self, widget, data=None):
        return not self.__close()

    # Funciones Internas ------------------------------------------------------

    def __validate(self, widget, textview):

        is_validated = True
        #TODO: Cambiar este textbuffer por un Entry con multilineas
        self.textbuffer = textview.get_buffer()
        start, end = self.textbuffer.get_bounds()
        self.dnota = self.textbuffer.get_text(start, end)

        # Validar Título
        if is_empty_string(self.txt_titulo.get_text()):
            is_validated = False

        # Validar Autor
        if is_empty_string(self.txt_autor.get_text()):
            is_validated = False

        # Validar Correo
        if not is_valid_email(self.txt_correo.get_text()):
            is_validated = False

        # Validar Descipción
        if is_empty_string(self.dnota):
            is_validated = False

        # Validar Captcha
        if  self.txt_captcha.get_text() != self.word:
            is_validated = False

        # Validar Opciones seleccionadas
        # Chequear internet

        return is_validated

        if self.txt_titulo.get_text():

            if self.txt_autor.get_text():

                if re.match('^[(a-z0-9\_\-\.)]+@[(a-z0-9\_\-\.)]+\.[(a-z)]{2,4}$', self.txt_correo.get_text().lower()):

                    if self.dnota:

                        #validacion del captcha
                        if  self.txt_captcha.get_text() != self.word:

                            md = gtk.MessageDialog(parent=None, flags=0, type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_CLOSE, message_format="El valor introducido no coincide con el captcha intente de nuevo")
                            md.run()
                            md.destroy()
                            self.refresh_captcha()
                            self.txt_captcha.set_text("")

                        else:
                            self.refresh_captcha()

                            ## Aqui se construia la nota

                            if (self.vdis == 0):
                                md = gtk.MessageDialog(parent=None, flags=0, type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_CLOSE, message_format="Por Favor!:\nSeleccione al menos una opción a consultar\ndel cuadro Seleccione datos a enviar.")
                                md.run()
                                md.destroy()

                            if (self.dnota == "" or self.vdis == 0 or self.txt_titulo.get_text() == "" or self.txt_autor.get_text() == ""):
                                md = gtk.MessageDialog(parent=None, flags=0, type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_CLOSE, message_format="No es posible enviar la nota o ver el informe.")
                                md.run()
                                md.destroy()

                            else:

                                if self.check_gdocum.get_active() == True:
                                    filedf = open(TXT_FILE, 'w')
                                    filedf.writelines(titulo_2)
                                    filedf.writelines(autor_2)
                                    filedf.writelines(info)
                                    filedf.close()
                                    worker = ThreadTxtEditor(self)
                                    worker.start()

                                else:

                                    def prueba_inter(self):
                                        os.system("wget -P /tmp http://www.google.co.ve/")
                                        t = next(os.walk('/tmp/'))[2]
                                        a = 'index.html'
                                        b = ''
                                        for b in t:
                                            if b == a:
                                                os.system('rm /tmp/index.html')
                                                return True
                                            else:
                                                pass

                                    if prueba_inter(self) == True:
                                        params = urllib.urlencode({'codigo_form': info, 'titulo_form': titulo_1, 'nombre_form': autor_1})
                                        f = urllib.urlopen("http://notas.canaima.softwarelibre.gob.ve/enviar_consola", params)
                                        self.mes = f.read()
                                        md = gtk.MessageDialog(parent=None, flags=0, type=gtk.MESSAGE_INFO, buttons=gtk.BUTTONS_CLOSE, message_format="El envio de la nota fue exitoso...!\n " + str(self.mes))
                                        md.run()
                                        md.destroy()
                                        worker = ThreadWebBrowser(self)
                                        worker.start()
                                    else:
                                        md = gtk.MessageDialog(parent=None, flags=0, type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_CLOSE, message_format="\tEl reporte no podrá ser enviado a la plataforma de \t\n\tCanaima, porque no posee una conexión a internet.\n\n\tPero puedo verlo en el sistema con la opción \n\tVer Documento (No Enviar).")
                                        md.set_title('Error en Conexión')
                                        md.run()
                                        md.destroy()
                                        self.check_gdocum.set_active(True)

                    else:
                        md = gtk.MessageDialog(parent=None, flags=0, type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_CLOSE, message_format="Por Favor!:\nTomese unos instantes y describa su situación o inconveniente\n en el Cuadro de Documentar Falla.")
                        md.run()
                        md.destroy()
                        self.refresh_captcha()

                else:
                    md = gtk.MessageDialog(parent=None, flags=0, type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_CLOSE, message_format="Es necesario que coloque una Dirección de correo electrónico.\n\n\t\t Ejemplo : correo@ejemplo.com")
                    md.run()
                    md.destroy()
                    self.refresh_captcha()
            else:
                md = gtk.MessageDialog(parent=None, flags=0, type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_CLOSE, message_format="Es necesario que coloque un txt_autor.")
                md.run()
                md.destroy()
                self.refresh_captcha()

        else:
            md = gtk.MessageDialog(parent=None, flags=0, type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_CLOSE, message_format="Es necesario que coloque un título.")
            md.run()
            md.destroy()
            self.refresh_captcha()

    def __is_viewonly(self):
        return self.check_gdocum.get_active()

    def __build_note(self):

        self.vdis = 0

        info = Note(self.txt_titulo.get_text(),
                    self.txt_autor.get_text(),
                    self.txt_correo.get_text(),
                    self.dnota)
        info.is_viewonly = self.__is_viewonly()

        if self.check_lspci.get_active() == True:
            command = "lspci"
            subtitle = "Dispositivos conectados por PCI"
            info.add_log_output(command, subtitle)
            self.vdis = 1

        if self.check_tm.get_active() == True:
            command = "lspci | grep 'Host bridge:'"
            subtitle = "Tarjeta Madre"
            info.add_log_output(command, subtitle)
            self.vdis = 1

        if self.check_lsusb.get_active() == True:
            command = "lsusb"
            subtitle = "Dispositivos conectados por puerto USB"
            info.add_log_output(command, subtitle)
            self.vdis = 1

        if self.check_acelgraf.get_active() == True:
            command = "glxinfo | grep -A4 'name of display:'"
            subtitle = "Aceleración gráfica"
            info.add_log_output(command, subtitle)
            self.vdis = 1

        if self.check_ired.get_active() == True:
            command = "cat /etc/network/interfaces"
            subtitle = "Información interfaces de RED"
            info.add_log_output(command, subtitle)
            self.vdis = 1

        if self.check_prefe.get_active() == True:
            command = "cat /etc/apt/preferences"
            subtitle = "Información /etc/apt/preferences"
            info.add_log_output(command, subtitle)
            self.vdis = 1

        if self.check_ram.get_active() == True:
            command = "free -m"
            subtitle = "Memoria RAM, Swap, y Buffer (en MB)"
            info.add_log_output(command, subtitle)
            self.vdis = 1

        if self.check_df.get_active() == True:
            command = "df -h"
            subtitle = "Espacio libre en los dispositivos de almacenamiento:\n\
S.ficheros| Tamaño Usado | Disp | Uso% | Montado en"
            info.add_log_output(command, subtitle)
            self.vdis = 1

        if self.check_tpart.get_active() == True:
            command = "fdisk -l"
            subtitle = "Tabla de particiónes"
            info.add_log_output(command, subtitle)
            self.vdis = 1

        if self.check_cpu.get_active() == True:
            command = "cat /proc/cpuinfo"
            subtitle = "Información del procesador"
            info.add_log_output(command, subtitle)
            self.vdis = 1

        if self.check_xorg.get_active() == True:
            command = "cat /var/log/Xorg.0.log | grep 'error'"
            subtitle = "Información de errores de Xorg"
            info.add_log_output(command, subtitle)
            self.vdis = 1

        if self.check_repo.get_active() == True:
            command = "cat /etc/apt/sources.list"
            subtitle = "Información de los repositorios"
            info.add_log_output(command, subtitle)
            self.vdis = 1

        if self.check_modu.get_active() == True:
            command = "lsmod"
            subtitle = "Listado de los modulos del kernel"
            info.add_log_output(command, subtitle)
            self.vdis = 1

        if self.check_vers.get_active() == True:
            command = "uname -a"
            subtitle = "Versión del Kernel"
            info.add_log_output(command, subtitle)
            self.vdis = 1

    def __close(self, widget=None):
        if self.txt_titulo.get_text() or self.txt_autor.get_text():
            md = message_question("Al cerrar, todos los procedimientos que \
            esté generando el Documentador de Fallas serán cerrados.\n\n\t\
            ¿Desea salir de la aplicación?", self)
            md.set_title('Cerrar')
            respuesta = md.run()
            md.destroy()

            if respuesta == gtk.RESPONSE_YES:
                os.system("rm %s" % IMG_CAPTCHA)
                self.destroy()
                gtk.main_quit()

        else:
            os.system("rm %s" % IMG_CAPTCHA)
            self.destroy()
            gtk.main_quit()

    def refresh_captcha(self):
        self.word = get_random_word()
        create_captcha_img(self.word.strip(), FONT_CAPTCHA, 20, IMG_CAPTCHA)
        self.img_captcha.set_from_file(IMG_CAPTCHA)


# Hilos -----------------------------------------------------------------------


class ThreadTxtEditor(threading.Thread):
    def __init__(self, mainview):
        threading.Thread.__init__(self)

    def run(self):
        os.system("gedit %s" % TXT_FILE)


class ThreadWebBrowser(threading.Thread):
    def __init__(self, mainview):
        threading.Thread.__init__(self)

    def run(self):
        os.system("sensible-browser %s" % URL_PASTE_PLATFORM)


if __name__ == "__main__":

    base = Main()
    gtk.main()
