#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Copyright (C) 2010 Canaima GNU/Linux
<desarrolladores@canaima.softwarelibre.gob.ve>

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA

@author: Erick Birbe <erickcion@gmail.com>
@author: Carlos Espinoza <carlosarmikhael@gmail.com>
@author: Francisco Vásquez <franjvasquezg@gmail.com>

'''

from common import ICON_PATH, TOP_BANNER_PATH, get_random_word, FONT_CAPTCHA, \
    IMG_CAPTCHA, create_captcha_img, TXT_FILE, URL_PASTE_PLATFORM, \
    launch_help, message_question, message_error, list_to_lines
import gtk
import os
import threading
from validations import is_empty_string, is_valid_email, have_internet_access
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
        # FIXME: Captcha sólo deberia aparecer si el contenido se va a enviar
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
        self.btn_aceptar.connect("clicked", self.on_btn_aceptar_clicked)

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

        else:
            self.check_acelgraf.set_active(False)
            self.check_xorg.set_active(False)
            self.check_repo.set_active(False)
            self.check_tpart.set_active(False)
            self.check_prefe.set_active(False)
            self.check_ired.set_active(False)

    def selectalldis3(self, widget, data=None):

        if self.check_all3.get_active() == True:

            self.check_vers.set_active(True)
            self.check_modu.set_active(True)

        else:
            self.check_vers.set_active(False)
            self.check_modu.set_active(False)

    # Eventos -----------------------------------------------------------------

    def on_btn_ayuda_clicked(self, widget=None):
        hilo = threading.Thread(target=launch_help, args=(self))
        hilo.start()

    def on_btn_aceptar_clicked(self, widget):
        errors = self.__validate_form()
        # Si la lista de errores contiene algo entonces no es valido.
        if errors != []:
            message_error(list_to_lines(errors))
            return False

        if self.__is_viewonly():
            self.note.write_to_file()
            worker = ThreadTxtEditor(self)
            worker.start()
        else:
            self.note.send_note()
            worker = ThreadWebBrowser(self)
            worker.start()

        self.refresh_captcha()
        return True

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

    def __validate_form(self):

        messages = []

        #TODO: Cambiar este textbuffer por un Entry con multilineas
        self.textbuffer = self.textview.get_buffer()
        start, end = self.textbuffer.get_bounds()
        self.dnota = self.textbuffer.get_text(start, end)

        # Validar título
        if is_empty_string(self.txt_titulo.get_text()):
            messages.append("- Es necesario que escriba un título.")

        # Validar Autor
        if is_empty_string(self.txt_autor.get_text()):
            messages.append("- Es necesario que escriba su nombre.")

        # Validar correo
        if not is_valid_email(self.txt_correo.get_text()):
            messages.append("- Es necesario que escriba su dirección de \
correo electrónico.")

        # Validar descipción
        if is_empty_string(self.dnota):
            messages.append("- Tómese unos instantes y describa la falla.")

        # Validar opciones seleccionadas
        if not self.__build_note():
            messages.append("- Seleccione al menos 1 opción del cuadro de \
Datos a Enviar.")

        # Validaciones sólo para el caso de enviar
        if not self.__is_viewonly():
            # Validar captcha
            if  self.txt_captcha.get_text() != self.word:
                messages.append("- El valor introducido no coincide con el de \
la imágen.")
            # Chequear internet
            if not have_internet_access():
                messages.append("- No posee una conexión a internet activa. \
Seleccione la opción No Enviar.")

        return messages

    def __is_viewonly(self):
        return self.check_gdocum.get_active()

    def __build_note(self):

        selection = False

        self.note = Note(self.txt_titulo.get_text(),
                    self.txt_autor.get_text(),
                    self.txt_correo.get_text(),
                    self.dnota)
        self.note.is_viewonly = self.__is_viewonly()

        if self.__is_viewonly():
            self.note.append_defaults()

        #TODO: Ordenar estos comandos desde lo mas general a lo mas especifico
        if self.check_lspci.get_active() == True:
            command = "lspci"
            subtitle = "Dispositivos conectados por PCI"
            self.note.add_log_output(command, subtitle)
            selection = True

        if self.check_tm.get_active() == True:
            command = "lspci | grep 'Host bridge:'"
            subtitle = "Tarjeta Madre"
            self.note.add_log_output(command, subtitle)
            selection = True

        if self.check_lsusb.get_active() == True:
            command = "lsusb"
            subtitle = "Dispositivos conectados por puerto USB"
            self.note.add_log_output(command, subtitle)
            selection = True

        if self.check_acelgraf.get_active() == True:
            command = "glxinfo | grep -A4 'name of display:'"
            subtitle = "Aceleración gráfica"
            self.note.add_log_output(command, subtitle)
            selection = True

        if self.check_ired.get_active() == True:
            command = "cat /etc/network/interfaces"
            subtitle = "Información interfaces de RED"
            self.note.add_log_output(command, subtitle)
            selection = True

        if self.check_prefe.get_active() == True:
            command = "cat /etc/apt/preferences"
            subtitle = "Información /etc/apt/preferences"
            self.note.add_log_output(command, subtitle)
            selection = True

        if self.check_ram.get_active() == True:
            command = "free -m"
            subtitle = "Memoria RAM, Swap, y Buffer (en MB)"
            self.note.add_log_output(command, subtitle)
            selection = True

        if self.check_df.get_active() == True:
            command = "df -h"
            subtitle = "Espacio libre en los dispositivos de almacenamiento:"
            self.note.add_log_output(command, subtitle)
            selection = True

        if self.check_tpart.get_active() == True:
            command = "fdisk -l"
            subtitle = "Tabla de particiones"
            self.note.add_log_output(command, subtitle)
            selection = True

        if self.check_cpu.get_active() == True:
            command = "cat /proc/cpuinfo"
            subtitle = "Información del procesador"
            self.note.add_log_output(command, subtitle)
            self.vdis = True

        if self.check_xorg.get_active() == True:
            command = "cat /var/log/Xorg.0.log | grep 'error'"
            subtitle = "Información de errores de Xorg"
            self.note.add_log_output(command, subtitle)
            selection = True

        if self.check_repo.get_active() == True:
            command = "cat /etc/apt/sources.list"
            subtitle = "Información de los repositorios"
            self.note.add_log_output(command, subtitle)
            selection = True

        if self.check_modu.get_active() == True:
            command = "lsmod"
            subtitle = "Listado de los modulos del kernel"
            self.note.add_log_output(command, subtitle)
            selection = True

        if self.check_vers.get_active() == True:
            command = "uname -a"
            subtitle = "Versión del Kernel"
            self.note.add_log_output(command, subtitle)
            selection = True

        return selection

    def __close(self, widget=None):
        if self.txt_titulo.get_text() or self.txt_autor.get_text():
            response = message_question("Al cerrar, todos los procedimientos \
que esté generando el Documentador de Fallas serán cerrados.\n\n\t \
¿Desea salir de la aplicación?", self)

            if response == gtk.RESPONSE_YES:
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

    wnd_form = Main()
    gtk.main()
