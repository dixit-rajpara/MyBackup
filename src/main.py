import os
import subprocess

from pathlib import Path
from datetime import datetime

TODAY = datetime.now().strftime('%Y-%m-%d_%H-%M')
PATH_SEP = os.path.sep
HOME_DIR = str(Path.home())
BACKUP_DIR = PATH_SEP + PATH_SEP.join(['dixit', 'LinuxBackups', 'My_Home_Backup_' + TODAY])

INCLUDE_LIST = [
    'Code', '.config', 'Desktop', 'Documents', 'Downloads', 'Music', '.PhpStorm2019.1', 'PhpstormProjects',
    'Pictures', '.PyCharmCE2018.3', 'PycharmProjects', '.ssh', 'Videos', '.bashrc-personal', '.dfsync.json',
    '.bash_aliases'
]

def create_dir(full_dir):
    try:
        os.makedirs(full_dir)
    except FileExistsError:
        # directory already exists
        pass

def add_dir_sep(path):
    return PATH_SEP.join(path)

def add_home_path(items):
    return list(map(lambda file : HOME_DIR + PATH_SEP + file, items))


def doRsync(src_path, dst_path):
    subprocess.run(["rsync", "-uah", "--stats", "--delete", "--info=progress2", src_path, dst_path])

def get_size(start_path='.'):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # skip if it is symbolic link
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)
    return total_size


if __name__ == '__main__':

    create_dir(BACKUP_DIR)

    backup_files = add_home_path(INCLUDE_LIST)
    backup_files = list(filter(os.path.exists, backup_files))

    totalPaths = len(backup_files)

    for i, backup_file in enumerate(backup_files):
        print("({}/{}) Backing up: {} ".format(i + 1, totalPaths, backup_file))
        doRsync(backup_file, BACKUP_DIR)
