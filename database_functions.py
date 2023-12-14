#database_functions.py

import os
import shutil
import datetime

backup_dir = 'backup_database'
source_dir = 'database'
max_backups = 15  # Define the maximum number of backups you want to keep

def delete_oldest_backups(backup_directory, max_backup_count):
    # Get a list of all backup files in the directory, sorted by date modified (oldest first)
    backup_files = sorted(
        [f for f in os.listdir(backup_directory) if os.path.isfile(os.path.join(backup_directory, f))],
        key=lambda f: os.path.getmtime(os.path.join(backup_directory, f))
    )

    # Calculate the number of backups to delete
    excess_backup_count = len(backup_files) - max_backup_count
    # Delete the oldest backups if necessary
    for i in range(excess_backup_count):
        os.remove(os.path.join(backup_directory, backup_files[i]))
        #print(f"Deleted old backup: {backup_files[i]}")

def backup_database():
    # Ensure the backup directory exists
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    # Generate a timestamp for the backup file
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

    # Iterate through the database files and copy them to the backup directory
    for filename in os.listdir(source_dir):
        if filename.endswith('.dat') or filename.endswith('.dir') or filename.endswith('.bak'):
            source_path = os.path.join(source_dir, filename)
            backup_path = os.path.join(backup_dir, f"{timestamp}_{filename}")

            shutil.copy2(source_path, backup_path)
            #print(f"Backup created: {backup_path}")

    # Delete older backups if necessary
    delete_oldest_backups(backup_dir, max_backups)

