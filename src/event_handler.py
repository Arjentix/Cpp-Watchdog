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
import re

class EventHandler(FileSystemEventHandler):
    def __init__(self, observer, window, params):
        self._observer = observer
        self._window = window
        self._params = params
        self._ignore_patterns = []
        if isinstance(params['ignore'], str):
            self._ignore_patterns.append(re.compile(params['ignore']))
        elif isinstance(params['ignore'], list):
            for regex in params['ignore']:
                self._ignore_patterns.append(re.compile(regex))

    def on_any_event(self, event = None):
        with self._observer.ignore_events():
            if event is not None:
                for pattern in self._ignore_patterns:
                    if pattern.match(event.src_path):
                        return

            self._window.display_build_start()
            completed_proc = subprocess.run(
                self._params['build_command'].split(),
                capture_output=True)
            self._window.display_build_status(completed_proc.returncode)

            if completed_proc.returncode == 0:
                result_file = '/tmp/watchdog_test_results.json'
                devnull = open(os.devnull, 'w')
                completed_proc = subprocess.run([self._params['test_bin'], f'--gtest_output=json:{result_file}'], stdout=devnull)

                with open(result_file) as json_file:
                    try:
                        test_results = json.load(json_file)
                        self._window.display_tests(test_results)
                    except json.decoder.JSONDecodeError as e:
                        print("Error: ", e)
                os.remove(result_file)
            else:
                if (self._get_cmake_generator() == 'Ninja'):
                    self._window.display_build_output(completed_proc.stdout)
                else:
                    self._window.display_build_output(completed_proc.stderr)

    def _get_cmake_generator(self):
        return subprocess.check_output("cat build/CMakeCache.txt | grep CMAKE_GENERATOR:INTERNAL= | sed 's/^.*=//'", shell=True).decode().strip()
