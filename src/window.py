import curses
from threading import Thread
import time
import json

class Window:
    def __init__(self):
        self._screen = curses.initscr()
        curses.noecho()
        self._screen.refresh()

        self.BUILD_STATUS_POS = (0, 10)
        self.OUTPUT_POS = (3, 0)
    
    def __del__(self):
        text = ''
        for y in (0, 10):
            text += self._screen.getstr(y, 0).decode(encoding='utf-8')
        curses.echo()
        curses.endwin()
        print(text)
    
    def display_build_start(self):
        self._building = True
        self._screen.clear()
        self._screen.addstr('Building: ')
        self._thread = Thread(target=self._twirl_stick)
        self._thread.start()
    
    def display_build_status(self, status):
        self._building = False
        self._thread.join()
        self._screen.move(self.BUILD_STATUS_POS[0], self.BUILD_STATUS_POS[1])
        self._screen.delch()
        if status == 0:
            self._screen.addstr('✓')
        else:
            self._screen.addstr('🞪')
        
        self._screen.refresh()

    def display_build_output(self, output):
        self._screen.move(self.OUTPUT_POS[0], self.OUTPUT_POS[1])
        self._screen.addstr(output)
        self._screen.refresh()
        return

    def display_tests(self, test_results):
        self._screen.move(self.OUTPUT_POS[0], self.OUTPUT_POS[1])

        self._screen.addstr('Total: ' + str(test_results['tests'] - test_results['failures']) +
                            '/' + str(test_results['tests']) + 
                            ' (' + test_results['time'] + ')\n')

        for testsuite in test_results['testsuites']:
            info = '✓'
            if testsuite['failures'] > 0:
                info = '🞪'
            info += (' ' + testsuite['name'] +
                     ': ' + str(testsuite['tests'] - testsuite['failures']) + '/' + str(testsuite['tests']) +
                     ' (' + test_results['time'] + ')\n')
            self._screen.addstr(info)
            for real_testsuite in testsuite['testsuite']:
                self._screen.addstr('    ' + self._get_test_info(real_testsuite) + '\n')

        self._screen.refresh()

    def _twirl_stick(self):
        chars = ['/', '-', '\\']

        i = 0
        while self._building:
            self._screen.move(self.BUILD_STATUS_POS[0], self.BUILD_STATUS_POS[1])
            self._screen.delch()
            self._screen.addch(chars[i])
            self._screen.refresh()
            i += 1
            if i == len(chars):
                i = 0
            time.sleep(0.2)

    def _get_test_info(self, testsuite):
        info = '✓'
        if 'failures' in testsuite:
            info = '🞪'
        
        info += (' ' + testsuite['name'] +
                 ' (' + testsuite['time'] + ')')

        return info
