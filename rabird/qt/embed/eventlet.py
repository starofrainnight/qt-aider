
import eventlet
import functools
from eventlet import hubs
from qtpy.QtCore import QTimer


def getMinTimerClock():
    hub = hubs.get_hub()

    currentClock = hub.clock()
    defaultMinClock = 3600
    minClock = defaultMinClock
    for scheduledClock, _ in hub.timers:
        deltaClock = scheduledClock - currentClock
        if deltaClock < 0.0:
            continue

        if deltaClock < minClock:
            minClock = deltaClock

    # We run time for each 100ms if don't have any
    if minClock == defaultMinClock:
        minClock = 0.1

    return minClock


def _timerOnTimeout(timer):
    eventlet.sleep(0)
    timer.setInterval(getMinTimerClock() * 1000)
    timer.start()


def embed(aQObject):
    tag = "__eventletEmbededTimer__"

    timer = QTimer()
    timer.setSingleShot(True)
    timer.setInterval(0.1)
    timer.timeout.connect(functools.partial(_timerOnTimeout, timer))
    timer.start()

    aQObject.setProperty(tag, timer)
