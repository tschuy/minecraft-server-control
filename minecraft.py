#!/usr/bin/python3
import shutil
from os.path import join
import os
import time
import sys
import datetime

WEEK = 604800
DAY = 86400

# Location of the Minecraft server installation.
# It's assumed that the world is stored in the world subdirectory.
minecraft_dir = '/opt/minecraft/'
world_dir = join(minecraft_dir, 'world')


# A list of backup directories. Each of these directories will hold three
# backups from the last 15 minutes, one from the previous day, and one
# from the previous week.
backup_directories = ['/opt/minecraft/backups',
                      '/media/external/Backups/Minecraft']

def server_command(cmd):
    os.system('screen -S minecraft -X stuff "{}\015"'.format(cmd))

def backup():
    server_command('save-off')
    server_command('save-all')

    time.sleep(5)
    # Do the backup magic
    current_time = datetime.datetime.now()
    # Replace colons with periods for NTFS compatibility
    time_string = current_time.isoformat().replace(':', '.')

    print("Creating archive...")
    shutil.make_archive('/tmp/{}'.format(time_string), 'gztar', world_dir)

    for backup_dir in backup_directories:

        # Create new backup
        try:
            print("Copying to {}".format(backup_dir))
            shutil.copy(
                '/tmp/{}.tar.gz'.format(time_string),
                join(backup_dir,
                '{}.tar.gz'.format(time_string)))
        except PermissionError as e:
            print('permission error')

        # Delete old backups
        for backup in os.listdir(backup_dir):
            # Get age of backup in seconds
            creation_time = os.stat(join(backup_dir, backup)).st_mtime
            age = time.mktime(
                datetime.datetime.now().timetuple()) - creation_time

            # Remove backups older than a week, and any backup not made within
            # 300 seconds/5 minutes of the beginning of the day
            if age > WEEK or (age > 1000 and creation_time % DAY > 300):
                print("Removing backup {}/{}".format(backup_dir, backup))
                shutil.rmtree(join(backup_dir, backup))
    server_command('save-on')
    print("Backups complete.")


def start():
    if not status():
        os.chdir(minecraft_dir)
        os.system('screen -dmS "minecraft" java -Xmx1024M -Xms1024M -jar minecraft_server.jar nogui')
        print("Server started.")
    else:
        print("Server already started.")

def stop():
    if status():
        server_command('stop')
        print("Server stopped.")
    else:
        print("Server not running.")

def status():
    output = os.popen('screen -ls').read()
    if '.minecraft'  in output:
        print("Server is running.")
        return True
    else:
        print("Server is not running.")
        return False

def main():
    if sys.argv[1] == 'start':
        start()
    elif sys.argv[1] == 'stop':
        stop()
    elif sys.argv[1] == 'backup':
        backup()
    elif sys.argv[1] == 'status':
        status()
    else:
        print('Unknown command {}. Please run {} [start/stop/backup/status].'.format(
            sys.argv[1], sys.argv[0]))


if __name__ == "__main__":
    main()
