'''
@author: Polyakov Daniil
@mail: arjentix@gmail.com
@github: Arjentix
@date: 30.07.20
'''

import sys
import pyinotify
import getopt
import subprocess

build_command = ''

def get_args(argv):
    home = '.'
    build_command = ''
    files = [home]

    optlist, args = getopt.getopt(argv, 'h:b:', ['home=', 'build-command='])
    for opt, arg in optlist:
        if opt in ('-h', '-home'):
            home = arg
        elif opt in ('-b', '--build-command'):
            build_command = arg

    if build_command == '':
        build_command = f'/usr/bin/cmake --no-warn-unused-cli -DCMAKE_EXPORT_COMPILE_COMMANDS:BOOL=TRUE -DCMAKE_BUILD_TYPE:STRING=Debug -DCMAKE_CC_COMPILER:FILEPATH=/usr/bin/g++ -DCMAKE_CXX_COMPILER:FILEPATH=/usr/bin/g++ -H{home} -B{home}/build'
    if len(args) != 0:
        files = args

    return [build_command, files]

def event_handler(event):
    global build_command

    completed_proc = subprocess.run(build_command.split())
    print(f'Build returned: {completed_proc.returncode}')

if __name__ == "__main__":
    build_command, files = get_args(sys.argv[1:])

    # Setting files event handler
    wm = pyinotify.WatchManager()
    notifier = pyinotify.Notifier(wm, event_handler)
    for file in files:
        wm.add_watch(file, pyinotify.IN_CLOSE_WRITE | pyinotify.IN_DELETE |
                           pyinotify.IN_DELETE_SELF | pyinotify.IN_MOVE_SELF|
                           pyinotify.IN_MOVED_FROM | pyinotify.IN_MOVED_TO)

    try:
        notifier.loop(
            daemonize=False
        )
    except pyinotify.NotifierError as err:
        print(err, file=sys.stderr)
