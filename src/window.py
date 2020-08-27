import curses
import sys
from threading import Thread
import time

class Window:
    def __init__(self):
        self._screen = curses.initscr()
        curses.start_color()
        curses.use_default_colors()

        if not curses.has_colors() or curses.COLORS < 8:
            print('Can\'t display colors. Terminating...')
            sys.exit()

        curses.noecho()
        self._screen.refresh()
        self._screen.scrollok(True)

        self.BUILD_STATUS_POS = (0, 10)
        self.OUTPUT_POS = (2, 0)

        # curses.init_color(8, 128, 128, 128)
        curses.init_color(8, 119, 136, 153)

        curses.init_pair(1, curses.COLOR_RED, -1)
        curses.init_pair(2, curses.COLOR_GREEN, -1)
        curses.init_pair(3, curses.COLOR_WHITE, -1)
        curses.init_pair(4, curses.COLOR_CYAN, -1)
        curses.init_pair(5, 8, -1)

        self.ERROR_ATTR = curses.color_pair(1)
        self.OK_ATTR = curses.color_pair(2)
        self.TESTSUITE_ATTR = curses.color_pair(3)
        self.TEST_ATTR = curses.color_pair(4)
        self.TEST_FAIL_ATTR = curses.color_pair(5)
        self.IMPORTANT_ATTR = curses.color_pair(3) | curses.A_BOLD
        self.BUILD_ERROR_ATTR = curses.color_pair(3)
        self.BASIC_TEXT = curses.color_pair(5)

        self.KEY_ENTER = curses.KEY_ENTER
        self._key_to_handler = {}
        self._key_to_description = {}
        self._alive = True
        self._input_thread = Thread(target=self._process_input)
        self._input_thread.start()
    
    def __del__(self):
        curses.echo()
        curses.endwin()

    def stop(self):
        self._alive = False
        self._building = False
    
    def add_key_handler(self, key_code, handler):
        self._key_to_handler[key_code] = handler
    
    def add_key_description(self, key_str, description):
        self._key_to_description[key_str] = description
    
    def display_build_start(self):
        self._building = True
        self._screen.clear()
        self._screen.addstr('Building: ', self.IMPORTANT_ATTR)
        self._twirl_thread = Thread(target=self._twirl_stick)
        self._twirl_thread.start()
    
    def display_build_status(self, status):
        self._building = False
        self._twirl_thread.join()
        self._screen.move(self.BUILD_STATUS_POS[0], self.BUILD_STATUS_POS[1])
        self._screen.delch()
        self._display_status(status == 0, curses.A_BOLD)

    def display_build_output(self, output):
        self._screen.move(self.OUTPUT_POS[0], self.OUTPUT_POS[1])
        self._screen.addstr(output, self.BUILD_ERROR_ATTR)
        self._print_hotkeys()
        self._screen.refresh()
        return

    def display_tests(self, test_results):
        def get_score_and_time(testsuite):
            return (str(testsuite['tests'] - testsuite['failures']) +
                    '/' + str(testsuite['tests']) + 
                    ' (' + testsuite['time'] + ')')

        self._screen.move(self.OUTPUT_POS[0], self.OUTPUT_POS[1])
        self._screen.addstr('Total: ' + get_score_and_time(test_results) + '\n\n')

        for testsuite in test_results['testsuites']:
            self._display_status(testsuite['failures'] == 0)

            info = (' ' + testsuite['name'] +
                     ': ' + get_score_and_time(testsuite) + '\n')
            self._screen.addstr(info, self.TESTSUITE_ATTR)
            for test in testsuite['testsuite']:
                self._screen.addstr('    ')
                self._print_test_info(test)

        self._print_hotkeys()
        self._screen.refresh()

    def _display_status(self, is_ok, attribute = 0):
        if is_ok:
            self._screen.addstr('✓', self.OK_ATTR | attribute)
        else:
            self._screen.addstr('✗', self.ERROR_ATTR | attribute)
        self._screen.refresh()

    def _process_input(self):
        while self._alive:
            c = self._screen.getch()
            if c in self._key_to_handler:
                self._key_to_handler[c]()
            time.sleep(0.2)

    def _twirl_stick(self):
        chars = ['/', '-', '\\']

        i = 0
        while self._building:
            self._screen.move(self.BUILD_STATUS_POS[0], self.BUILD_STATUS_POS[1])
            self._screen.delch()
            self._screen.addch(chars[i], self.IMPORTANT_ATTR)
            self._screen.refresh()
            i += 1
            if i == len(chars):
                i = 0
            time.sleep(0.2)

    def _print_test_info(self, test):
        failed = False
        if 'failures' in test:
            failed = True

        self._display_status(not failed)
        
        self._screen.addstr(' ' + test['name'] +
                            ' (' + test['time'] + ')', self.TEST_ATTR)

        if failed:
            self._screen.addstr(':', self.TEST_ATTR)
            for failure in test['failures']:
                self._screen.addstr('\n        • ', self.ERROR_ATTR)
                info = failure['failure']

                # Adding some tabs for beauty
                start_pos = info.find('\n')
                while start_pos != -1:
                    info = info[0 : start_pos + 1] + '          ' + info[start_pos + 1:]
                    start_pos = info.find('\n', start_pos + 1)
                self._screen.addstr(info, self.TEST_FAIL_ATTR)

        self._screen.addch('\n')
    
    def _print_hotkeys(self):
        for key, description in self._key_to_description.items():
            self._screen.addstr('\nPress ', self.BASIC_TEXT)
            self._screen.addstr(key, self.IMPORTANT_ATTR)
            self._screen.addstr(' to ' + description, self.BASIC_TEXT)
