# -*- coding: utf-8 -*-

import sys
import qtpy
import whichcraft
import os.path


def getToolPath(name):
    if qtpy.API in qtpy.PYQT5_API:
        import PyQt5 as qtmodule

        tools = {
            'uic': 'pyuic5',
            'rcc': 'pyrcc5',
            'lupdate': 'pylupdate5',
        }

    elif qtpy.API in qtpy.PYSIDE2_API:
        import PySide2 as qtmodule

        tools = {
            'uic': 'pyside-uic',
            'rcc': 'pyside-rcc',
            'lupdate': 'pyside-lupdate',
        }

    elif qtpy.API in qtpy.PYQT4_API:
        import PyQt4 as qtmodule

        tools = {
            'uic': 'pyuic4',
            'rcc': 'pyrcc4',
            'lupdate': 'pylupdate4',
        }

    elif qtpy.API in qtpy.PYSIDE_API:
        import PySide as qtmodule

        tools = {
            'uic': 'pyside-uic',
            'rcc': 'pyside-rcc',
            'lupdate': 'pyside-lupdate',
        }

    suffixs = [""]
    if sys.platform == "win32":
        suffixs = ["", ".exe"]

    if name in tools:
        name = tools[name]

        qtModuleDir = os.path.dirname(qtmodule.__file__)
        for suffix in suffixs:
            toolPath = os.path.join(qtModuleDir, "%s%s" % (name, suffix))
            if os.path.exists(toolPath):
                return toolPath

    toolPath = whichcraft.which(name)
    if toolPath:
        return toolPath

    raise FileNotFoundError("Can't find this tool : %s" % name)
