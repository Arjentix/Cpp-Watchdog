'''
@author: Polyakov Daniil
@mail: arjentix@gmail.com
@github: Arjentix
@date: 27.08.20
'''

'''
This code was written by Ryne Everett
See: https://stackoverflow.com/questions/18781239/python-watchdog-is-there-a-way-to-pause-the-observer
'''

import time
import contextlib
import watchdog.observers


class PausingObserver(watchdog.observers.Observer):
    def dispatch_events(self, *args, **kwargs):
        if not getattr(self, '_is_paused', False):
            super(PausingObserver, self).dispatch_events(*args, **kwargs)

    def pause(self):
        self._is_paused = True

    def resume(self):
        time.sleep(self.timeout)  # allow interim events to be queued
        self.event_queue.queue.clear()
        self._is_paused = False

    @contextlib.contextmanager
    def ignore_events(self):
        self.pause()
        yield
        self.resume()
