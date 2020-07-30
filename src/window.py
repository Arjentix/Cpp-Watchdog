import curses
from threading import Thread
import time

class Window:
    def __init__(self):
        self._screen = curses.initscr()
        curses.noecho()
        self._screen.refresh()
    
    def __del__(self):
        # print('Bye')
        curses.echo()
        curses.endwin()
    
    def display_build_start(self):
        self._building = True
        self._screen.clear()
        self._screen.addstr('Building: ')
        self._thread = Thread(target=self._twirl_stick)
        self._thread.start()
    
    def display_build_res(self, res):
        self._building = False
        self._thread.join()
        self._screen.move(0, 10)
        self._screen.delch()
        if res == 0:
            self._screen.addstr('✓')
        else:
            self._screen.addstr('🞪')
        
        self._screen.refresh()

    def display_tests(self, tests_str):
        self._screen.move(5, 0)
        self._screen.addstr('Tests...')
        self._screen.refresh()

    def _twirl_stick(self):
        chars = ['/', '-', '\\']

        i = 0
        while self._building:
            self._screen.move(0, 10);
            self._screen.delch()
            self._screen.addch(chars[i])
            self._screen.refresh();
            i += 1
            if i == len(chars):
                i = 0
            time.sleep(0.2)
