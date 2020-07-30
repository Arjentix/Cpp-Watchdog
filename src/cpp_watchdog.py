'''
@author: Polyakov Daniil
@mail: arjentix@gmail.com
@github: Arjentix
@date: 30.07.20
'''

import sys
import pyinotify

def event_handler(event):
    print(f'Something happened: {event}')

if __name__ == "__main__":
    files = sys.argv[1:]
    if len(files) == 0:
        files.append('.') # Setting current dir as default

    # Setting files event handler
    wm = pyinotify.WatchManager()
    notifier = pyinotify.Notifier(wm, event_handler)
    for file in files:
        wm.add_watch(file, pyinotify.IN_CREATE | pyinotify.IN_DELETE |
                           pyinotify.IN_DELETE_SELF | pyinotify.IN_MOVE_SELF|
                           pyinotify.IN_MOVED_FROM | pyinotify.IN_MOVED_TO |
                           pyinotify.IN_CLOSE_WRITE)

    try:
        notifier.loop(
            daemonize=False
        )
    except pyinotify.NotifierError as err:
        print(err, file=sys.stderr)
