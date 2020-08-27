'''
@author: Polyakov Daniil
@mail: arjentix@gmail.com
@github: Arjentix
@date: 22.08.20
'''

from watchdog.events import FileSystemEventHandler
import subprocess
import os 
import json
import time 
import traceback

class EventHandler(FileSystemEventHandler):
    def __init__(self, observer, window, build_command, test_bin):
        self._observer = observer
        self._window = window
        self._build_command = build_command
        self._test_bin = test_bin

    def on_any_event(self, event = None):
        with self._observer.ignore_events():
            self._window.display_build_start()
            completed_proc = subprocess.run(self._build_command.split(), capture_output=True)
            self._window.display_build_status(completed_proc.returncode)

            if completed_proc.returncode == 0:
                result_file = '/tmp/watchdog_test_results.json'
                devnull = open(os.devnull, 'w')
                completed_proc = subprocess.run([self._test_bin, f'--gtest_output=json:{result_file}'], stdout=devnull)

                with open(result_file) as json_file:
                    test_results = json.load(json_file)
                    self._window.display_tests(test_results)
                os.remove(result_file)            
            else:
                self._window.display_build_output(completed_proc.stderr)
