import functools
import struct
from qtpy.QtCore import Signal
from qtpy.QtCore import QObject
from qtpy.QtCore import QSharedMemory
from qtpy.QtCore import QSystemSemaphore
from qtpy.QtNetwork import QLocalServer
from qtpy.QtNetwork import QLocalSocket


class SingleWorld(QObject):
    """
    SingleWorld is a class that wrap around the single application
    framework.
    """

    # Modes
    (
        # Server mode indicated that we started the first application
        Server,
        # Client mode means that another App already started, we should just
        # exit or send some message to that App before exit.
        Client,
    ) = range(0, 2)

    # Signals

    receivedMessage = Signal(bytes)

    def __init__(self, name, parent=None):
        super().__init__(parent)
        self._name = name
        self._mode = self.Server
        self._sharedMemory = QSharedMemory(self._name)
        self._systemSemaphore = QSystemSemaphore(self._name + "-2", 1)
        self._server = None
        self._client = None
        self._localSockets = {}

        # Fix for *nix:
        # http://stackoverflow.com/questions/5006547/qt-best-practice-for-a-single-instance-app-protection
        # http://habrahabr.ru/post/173281/

        self._systemSemaphore.acquire()
        try:
            unixFix = QSharedMemory(self._name)
            unixFix.attach()
            unixFix.detach()
            unixFix = None
        finally:
            self._systemSemaphore.release()

    @property
    def name(self):
        return self._name

    @property
    def mode(self):
        return self._mode

    def _onLocalSocketReadyRead(self, localSocket):
        if localSocket.bytesAvailable() <= 0:
            return

        self._localSockets[localSocket] += localSocket.readAll()
        data = self._localSockets[localSocket]
        if len(data) > 4:
            # First 4bytes is an native Integer.
            dataSize = struct.unpack("@I", data[:4])[0]
            receivedDataSize = len(data) - 4
            if receivedDataSize < dataSize:
                return

            self.receivedMessage.emit(bytes(data[4:]))

            # Remove the command socket
            del self._localSockets[localSocket]
            localSocket.deleteLater()

    def _onServerNewConnection(self):
        while self._server.hasPendingConnections():
            localSocket = self._server.nextPendingConnection()
            self._localSockets[localSocket] = b""
            localSocket.readyRead.connect(functools.partial(
                self._onLocalSocketReadyRead, localSocket))

    def start(self):
        # Ensure we run only one application
        isAnotherRunning = False
        if not self._sharedMemory.isAttached():
            # If share memory is attachable, that means there have another
            # running application
            self._systemSemaphore.acquire()
            try:
                isAnotherRunning = self._sharedMemory.attach()
                if isAnotherRunning:
                    self._sharedMemory.detach()
            finally:
                self._systemSemaphore.release()

        if not isAnotherRunning:
            # If we already attached by previous attach test, we will create
            # the share memory.
            self._systemSemaphore.acquire()
            try:
                isAnotherRunning = not self._sharedMemory.create(
                    1, QSharedMemory.ReadWrite)
            finally:
                self._systemSemaphore.release()

            # If there something happened during create procedure lead us can't
            # create one, we should detach that share memory.
            if isAnotherRunning:
                self._systemSemaphore.acquire()
                try:
                    if self._sharedMemory.isAttached():
                        self._sharedMemory.detach()
                finally:
                    self._systemSemaphore.release()

        # Fine, now we could take different action on different situation.
        if not isAnotherRunning:
            self._mode = self.Server
            self._server = QLocalServer(self)
            self._server.newConnection.connect(self._onServerNewConnection)

            if not self._server.listen(self._name):
                # Failed to listen, is there have another application crashed
                # without normally shutdown it's server?
                #
                # We try to remove the old dancing server and restart a new
                # server.
                self._server.removeServer(self._name)
                if not self._server.listen(self._name):
                    raise RuntimeError(
                        "Local server failed to listen on '%s'" % self._name)
        else:
            # Detach immediately if create failed.
            #
            # WARNING: On windows os, seems if we don't detach the share memory
            # after failed to create, another instance can't create the share
            # memory after original instance exitted while there still have
            # instance as client.

            self._mode = self.Client
            self._client = QLocalSocket(self)
            self._client.connectToServer(self._name)

    def sendMessage(self, message):
        # Only accept bytes message
        assert(type(message) == bytes)
        data = struct.pack("@I%ss" % len(message), len(message), message)
        self._client.write(data)
