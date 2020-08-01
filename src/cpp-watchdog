#!/usr/bin/env python3

'''
@author: Polyakov Daniil
@mail: arjentix@gmail.com
@github: Arjentix
@date: 30.07.20
'''

from window import Window

import sys
import os 
import pyinotify
import getopt
import subprocess
import json

window = Window()
build_command = ''
test_bin = ''

def get_args(argv):
    home = '.'
    build_command = ''
    test_bin = f'{home}/build/test/test'
    files = [home]

    optlist, args = getopt.getopt(argv, 'h:b:t:', ['home=', 'build-command=', 'test-bin='])
    for opt, arg in optlist:
        if opt in ('-h', '-home'):
            home = arg
        elif opt in ('-b', '--build-command'):
            build_command = arg
        elif opt in ('-t', '--test-bin'):
            test_bin = arg

    if build_command == '':
        build_command = '/usr/bin/cmake --build build --config Debug --target all -- -j 10'
    if len(args) != 0:
        files = args

    return [build_command, test_bin, files]

def event_handler(event):
    global window, build_command

    window.display_build_start()
    completed_proc = subprocess.run(build_command.split(), capture_output=True)
    window.display_build_status(completed_proc.returncode)

    if completed_proc.returncode == 0:
        result_file = 'watchdog_test_results.json'
        devnull = open(os.devnull, 'w')
        completed_proc = subprocess.run([test_bin, f'--gtest_output=json:{result_file}'], stdout=devnull)

        with open(result_file) as json_file:
            test_results = json.load(json_file)
            window.display_tests(test_results)
        os.remove(result_file)            

    else:
        window.display_build_output(completed_proc.stderr)

if __name__ == "__main__":
    build_command, test_bin, files = get_args(sys.argv[1:])

    # Initial run
    event_handler(None)

    # Setting files event handler
    wm = pyinotify.WatchManager()
    notifier = pyinotify.Notifier(wm, event_handler)
    for file in files:
        wm.add_watch(file, pyinotify.IN_CLOSE_WRITE | pyinotify.IN_DELETE |
                           pyinotify.IN_DELETE_SELF | pyinotify.IN_MOVE_SELF |
                           pyinotify.IN_MOVED_FROM | pyinotify.IN_MOVED_TO)

    try:
        notifier.loop(
            daemonize=False
        )
    except pyinotify.NotifierError as err:
        del window
        print(err, file=sys.stderr)
