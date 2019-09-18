# -*- coding: utf-8 -*-

def serverClassFactory(serverIface):
    from .FontLoader import FontLoaderServer
    return FontLoaderServer(serverIface)
