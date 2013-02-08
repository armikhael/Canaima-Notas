#-*- coding: UTF-8 -*-
'''
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
import re


def is_empty_string(string):
    '''Check if an string is empty or not
    Arguments:
        string: The text to be validated
    Return:
        True if is empty, False if is not.
    '''

    if string.strip() == "":
        return True
    else:
        return False


def is_valid_email(string):
    ''' Check if an string is a valid email address.
    Arguments:
        string: The text to be validated
    Return:
        True if is a valid email address or False if is not.
    '''
    return re.match('^[(a-z0-9\_\-\.)]+@[(a-z0-9\_\-\.)]+\.[(a-z)]{2,4}$',
                string.lower())
