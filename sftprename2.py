from inotify_simple import INotify, flags, masks
import os
import shutil as sh
import logging as lg

# |-- TODO - Rotate log file daily
# |-- TODO - Max file size of 2MB
# |-- TODO - Keep 2 weeks of logs (01 - 13) before pruning

# Define watched directory for file changes - SFTP root
sftp_root = '/home/riley/sftpdir/'  # type: str

# Define log directory for logs
log_file =  '/tmp/inotify.log'

# Configuration of log file
lg.basicConfig(filename=log_file, level=lg.DEBUG, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

def recursively_watch(inotify, root_folder, flags):
    """Recursively watch all files and directories under the given root folder, not
    following links. Returns a dictionary that maps watch descriptors to filepaths."""
    watches = {}
    for folder, _, filenames in os.walk(root_folder):
        filepaths = [os.path.join(folder, filename) for filename in filenames]
        for path in [folder] + filepaths:
            try:
                wd = inotify.add_watch(folder, flags)
                watches[wd] = path
            except FileNotFoundError:
                # Broken link or deleted
                pass
    return watches

inotify = INotify()
watches = recursively_watch(inotify, sftp_root, masks.ALL_EVENTS)

while True:
    for event in inotify.read():
        print(event)
        for flag in flags.from_mask(event.mask):
            print('    ' + str(flag))
