# this is the main application

import datetime
from models import Topic, Review
from todoist_manager import TodoistManager
import shelve
import configurations
from gather_user_data_gui import gather_data
from metadata_manager import MetadataManager

todoist_manager = TodoistManager()
metadata_manager = MetadataManager('metadata.txt')
today = datetime.date.today()

last_access = metadata_manager.last_access_date()

if last_access == today:
    pass
else: # Return the reviews in Todoist back to the database
    print('Returning reviews from Todoist.')
    todoist_manager.return_reviews()

# **************************************************************************************************
def add_topic_to_database():
    last_code_used = metadata_manager.last_code_used()
    code = str(int(last_code_used) + 1)
    metadata_manager.increase_last_code_used()

    data = gather_data()
    topic_obj = Topic(code=code, **data)
    topic_obj.create_review_objects()

    with shelve.open('database\\database', writeback=False) as db:
        db[code] = topic_obj
        print("Topic sucessfully stored in database.")
    return

def delete_topic_from_database():
    pass

def delete_specific_problem():
    pass

# *******************************************************************************************************
options_dictionary = {}

options_dictionary['1'] = add_topic_to_database
options_dictionary['2'] = todoist_manager.send_reviews_from_database

def main():
    while True:
        print('\n*******************Review Scheduler 5.0**********************')
        print('What would you like to do? [type the number of the option]')
        print('(1) Add review to database')
        print('(2) Transfer today\'s review to Todoist')
        print('(3) Database options')
        print('(4) Advanced options')
        print('(5) Exit application')
        

        ans = input()

        if ans == '5':
            input('Type anything to exit.')
            return 
        
        else:
            try:
                options_dictionary[ans]()
            except KeyError:
                print("Option not implemented yet.")

    
main()


    







