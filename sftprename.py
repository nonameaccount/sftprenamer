import logging as lg
import shutil as sh
from inotify_simple import INotify, flags

# variable to control while loop - Infinite Loop
var = 1

# Define watched directory for file changes
watched_dir = '/home/riley/sftpdir/'  # type: str

# Configuration of log file
lg.basicConfig(filename='/tmp/inotify.log', level=lg.DEBUG, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

inotify = INotify()
watch_flags = flags.CLOSE_WRITE
wd = inotify.add_watch(watched_dir, watch_flags)

while var == 1 : #This constructs an infinite loop
    for event in inotify.read():  # type: object
        lg.debug(event)
        sh.move(watched_dir + event[3], watched_dir + event[3] + '.done')
        for flag in flags.from_mask(event.mask):
            lg.debug(str(flag))