#-*- coding: UTF-8 -*-
'''
Copyright (C) 2010 Canaima GNU/Linux
<desarrolladores@canaima.softwarelibre.gob.ve>

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Ucumari; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA

Created on 08/02/2013

@author: Erick Birbe <erickcion@gmail.com>
'''
import sys
from subprocess import Popen, PIPE
import random
import ImageFont
import Image
import ImageDraw
import ImageFilter
import gtk

# Declaraciones ---------------------------------------------------------------

WORKDIR = sys.path[0]
APP_NAME = 'canaima-notas-gnome'
TOP_BANNER_PATH = WORKDIR + '/img/banner-app-top.png'
ICON_PATH = WORKDIR + '/img/canaima-notas-icons.png'
# FIXME: Rutas de archivos temporales no optimas en ambientes multiusuarios
# si varios usuarios utilizan la herramienta a la vez se pueden mezclar los
# contenidos de los archivos
TXT_FILE = '/tmp/notas-document.txt'
IMG_CAPTCHA = '/tmp/notas-captcha.jpg'
FONT_CAPTCHA = '/usr/share/fonts/truetype/ttf-dejavu/DejaVuSans.ttf'
URL_PASTE_PLATFORM = 'http://notas.canaima.softwarelibre.gob.ve/'

# Funciones generales ---------------------------------------------------------


def launch_help(widget=None):

    Popen(["yelp /usr/share/gnome/help/%s/es/c-n.xml" % APP_NAME], \
              shell=True, stdout=PIPE)


def get_random_word(wordLen=6):
    word = ""
    allowedChars = "abcdefghijklmnopqrstuvwzyzABCDEFGHIJKLMNOPQRSTUVWZYZ012345\
6789"
    for i in range(0, wordLen):
        word = word + allowedChars[random.randint(0, 0xffffff) % \
                                   len(allowedChars)]
    return word


def create_captcha_img(text, fnt, fnt_sz, file_name, frmat='JPEG'):
    fgcolor = random.randint(0, 1)
    bgcolor = fgcolor ^ 0xffffff
    font = ImageFont.truetype(fnt, fnt_sz)
    dim = font.getsize(text)

    image = Image.new('RGB', (dim[0] + 5, dim[1] + 5), bgcolor)
    draw = ImageDraw.Draw(image)

    x, y = image.size
    r = random.randint
    for i in range(100):
        draw.rectangle((r(0, x), r(0, y), r(0, x), r(0, y)), \
                       fill=r(0, 0xffffff))

    draw.text((3, 3), text, font=font, fill=fgcolor)
    image = image.filter(ImageFilter.EDGE_ENHANCE_MORE)
    image.save(file_name, frmat)


def list_to_lines(the_list):
    '''Converts each value of a list in a string line and returns the
    concatenated text.
    Arguments:
        the_list: The list that will be converted.
    Return:
        The string composed of concatenated lines.'''
    data = ""
    i = 0
    for line in the_list:
        if i > 0:
            data += "\n"
        i += 1
        data += str(line)
    return data


# GTK Dialogs -----------------------------------------------------------------

def message_question(message, parent=None):
    msg_box = gtk.MessageDialog(parent=parent,
                             type=gtk.MESSAGE_QUESTION,
                             buttons=gtk.BUTTONS_YES_NO,
                             message_format=message)
    response = msg_box.run()
    msg_box.destroy()
    return response


def message_error(message, parent=None):
    msg_box = gtk.MessageDialog(parent=parent,
                             type=gtk.MESSAGE_ERROR,
                             buttons=gtk.BUTTONS_CLOSE,
                             message_format=message)
    response = msg_box.run()
    msg_box.destroy()
    return response
