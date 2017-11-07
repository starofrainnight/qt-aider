
import eventlet
import functools
from eventlet import hubs
from qtpy.QtCore import QTimer


def get_min_timer_clock():
    hub = hubs.get_hub()

    current_clock = hub.clock()
    default_min_clock = 3600
    min_clock = default_min_clock
    for scheduled_clock, _ in hub.timers:
        delta_clock = scheduled_clock - current_clock
        if delta_clock < 0.0:
            continue

        if delta_clock < min_clock:
            min_clock = delta_clock

    # We run time for each 100ms if don't have any
    if min_clock == default_min_clock:
        min_clock = 0.1

    return min_clock


def _timerOnTimeout(timer):
    eventlet.sleep(0)
    timer.setInterval(get_min_timer_clock() * 1000)
    timer.start()


def embed(aQObject):
    tag = "__eventletEmbededTimer__"

    timer = QTimer()
    timer.setSingleShot(True)
    timer.setInterval(0.1)
    timer.timeout.connect(functools.partial(_timerOnTimeout, timer))
    timer.start()

    aQObject.setProperty(tag, timer)
