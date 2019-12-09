from qgis.server import *
from qgis.core import *

from PyQt5.QtCore import *
from PyQt5.QtGui import QFontDatabase

# Path to extra fonts. All *.ttf files will be loaded.
import os
fontDir = "C:/fonts"

def Bytes(string):
    return bytes(string, 'utf8')

# Adds SERVICE=FONTLOADER support for listing which fonts are loaded by this plugin
class FontLoader(QgsServerFilter):
    def __init__(self, serverIface):
        super(FontLoader, self).__init__(serverIface)

    def responseComplete(self):
        request = self.serverInterface().requestHandler()
        params = request.parameterMap()
        if params.get('SERVICE', '').upper() == 'FONTLOADER':
            request.clear()
            request.setResponseHeader('Content-type', 'text/plain')
            request.clearBody()

            request.appendBody(Bytes('Fonts imported from: {}\n'.format(fontDir)))
            it = QDirIterator(fontDir)
            while (it.hasNext()):
                path = it.next()
                if path.endswith('.ttf'):
                    request.appendBody(Bytes(it.fileName()+'\n'))
            request.appendBody(Bytes('END\n'))

class FontLoaderServer:
    def __init__(self, serverIface):
        it = QDirIterator(fontDir)
        while (it.hasNext()):
            path = it.next()
            if path.endswith('.ttf'):
                QFontDatabase.addApplicationFont(path)

        self.serverIface = serverIface
        serverIface.registerFilter(FontLoader(serverIface), 100)
