'''
Created on 08/02/2013

@author: Erick Birbe
'''
import os


class Note():

    def __init__(self, title=None, author=None, email=None, details=None):
        '''
        Constructor
        '''
        self.__data = []
        self.title = title
        self.author = author
        self.email = email
        self.details = details
        self.is_viewonly = True

    def __str__(self):
        data = ""
        i = 0
        for line in self.__data:
            if i > 0:
                data += "\n"
            i += 1
            data += str(line)
        return data

    def add(self, string):
        self.__data.append(string)

    def add_log_output(self, command, subtitle=None):

        if subtitle:
            self.add("----- %s:" % subtitle)
        else:
            self.add("----- [%s]:" % command)

        self.add("")
        self.add(os.popen(command).read())
        self.add("")

    def append_defaults(self):
        assert self.title is not None
        assert self.author is not None
        assert self.email is not None
        assert self.details is not None

        if self.is_viewonly:
            self.add("TITULO: %s" % self.title)
            self.add("AUTOR: %s" % self.author)
            self.add("CORREO: %s" % self.email)

        self.add("")
        self.add("_____________________ NOTA DE USUARIO ____________________")
        self.add("")
        self.add(self.details)
        self.add("__________________________________________________________")

if __name__ == "__main__":
    n = Note()
    n.title = "Hi"
    n.author = "There"
    n.email = "How"
    n.details = "are you"
    n.append_defaults()
    print n
