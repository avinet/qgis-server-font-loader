from qgis.server import *
from qgis.core import *

from PyQt4.QtCore import *
from PyQt4.QtGui import QFontDatabase

# Path to extra fonts. All *.ttf files will be loaded.
fontDir = "C:/fonts"

# Adds SERVICE=FONTLOADER support for listing which fonts are loaded by this plugin
class FontLoader(QgsServerFilter):
    def __init__(self, serverIface):
        super(FontLoader, self).__init__(serverIface)

    def responseComplete(self):
        request = self.serverInterface().requestHandler()
        params = request.parameterMap()
        if params.get('SERVICE', '').upper() == 'FONTLOADER':
            request.clearHeaders()
            request.setHeader('Content-type', 'text/plain')
            request.clearBody()

            request.appendBody('Fonts to be imported:\n')
            it = QDirIterator(fontDir)
            while (it.hasNext()):
                path = it.next()
                if path.endswith('.ttf'):
                    request.appendBody(it.fileName())
                    request.appendBody("\n")
            request.appendBody('END\n')

class FontLoaderServer:
    def __init__(self, serverIface):
        it = QDirIterator(fontDir)
        while (it.hasNext()):
            path = it.next()
            if path.endswith('.ttf'):
                QFontDatabase.addApplicationFont(path)

        self.serverIface = serverIface
        serverIface.registerFilter(FontLoader(serverIface), 100)