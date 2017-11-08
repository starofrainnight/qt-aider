# -*- coding: utf-8 -*-

import signal
import logging
from . import eventlet as rqeventlet


class InitMixin(object):
    """
    This mixin use to fix QCoreApplication for python:

    1. Fixed can't break program by Ctrl+C
    2. Fixed installTranslator() won't take effect until we keep the
       translator's reference manually.
    3. Integrated with eventlet framework, so we could use coroutines!
    """

    def __init__(self):
        signal.signal(signal.SIGINT, signal.SIG_DFL)

        # Embed eventlet
        rqeventlet.embed(self)

        # FIXME: Just use to keep translators references for avoid they be
        # deleted at runtime.
        self._translators = []

    def installTranslator(self, translator):
        """
        Override installTranslator() of QCoreApplication, so the translator's
        references won't missing.
        """

        self._translators.append(translator)
        return super().installTranslator(translator)

    def removeTranslator(self, translator):
        """
        Override removeTranslator() of QCoreApplication
        """

        self._translators.remove(translator)
        return super().removeTranslator(translator)
