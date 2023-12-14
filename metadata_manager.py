# metadata_manager.py

import datetime
from date_provider import date_format

today = datetime.date.today()

class MetadataManager:

    def __init__(self, filename):
        self.filename = filename

    def last_access_date(self) -> datetime.date: 
        with open(self.filename, 'r') as metadata_file:
            last_access_string = metadata_file.readlines()[0][13:].strip()
            last_access = datetime.datetime.strptime(last_access_string, date_format).date()
        return last_access

    def last_code_used(self) -> str:
        with open(self.filename, 'r') as metadata_file:
            lines = metadata_file.readlines()
            last_code_used = lines[1][16:].strip()
        return last_code_used

    def increase_last_code_used(self): 
        with open(self.filename, 'r') as metadata_file:
            lines = metadata_file.readlines()

        with open(self.filename, 'w') as metadata_file:
            last_code = lines[1][16:].strip()
            new_code = str( int(last_code) + 1 )
            lines[1] = f'Last code used: {new_code}'
            metadata_file.writelines(lines)

    def update_last_access_date(self, new_date=None):
        with open(self.filename, 'r') as metadata_file:
            lines = metadata_file.readlines()

        with open(self.filename, 'w') as metadata_file:
            today_string = today.strftime(date_format)
            metadata_file.write(f'Last access: {today_string}\n')
            metadata_file.write(lines[1])
