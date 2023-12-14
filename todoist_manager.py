# todoist_manager.py

import datetime
from todoist_api_python.api import TodoistAPI
import shelve
from models import Topic, Review
import configurations
from date_provider import date_format
from metadata_manager import MetadataManager
from database_functions import backup_database

# This info should probably be saved in another file and be passed as arguments for the todoist manager
project_id =  # reviews project
api_token = #enter your todoist api key here



metadata_manager = MetadataManager('metadata.txt')
today = datetime.date.today()


class TodoistManager:

    def __init__(self):
        self.api = TodoistAPI(api_token)

    def retrieve_review(self, code, review_number):
        '''Return a given review in Todoist back to the database'''
        pass

    def add_review(self, review_obj):
        '''Add a single task to Todoist'''
        task = self.api.add_task(content=review_obj.content(), 
                                 description=review_obj.description(), 
                                 project_id=project_id, 
                                 due_string=today.strftime(date_format)
                                 )
        print('Adding review to Todoist')

        for problem in review_obj.problem_subset:
            subtask = self.api.add_task(content=problem, parent_id=task.id)
            print('.', end='')
        print('\nReview sucessfuly added to Todoist\n')

    def return_reviews(self):

        backup_database() 

        
        '''Returns all reviews in Todoist back to the database'''

        count = 0 # number of tasks returned

    
        # can be made into a function
        try:
            task_list = self.api.get_tasks(project_id=project_id) #all the tasks in Todoist including subtasks
        except Exception as E:
            print(f'{today}', "Something went wrong while trying to fetch reviews from Todoist, it might be your internet connection. No review was returned to database. Try again later.")
            print(E, file=open('error_log.txt', 'a') )
            return 

        if not task_list: # No reviews in Todoist
            print('No reviews were found in Todoist')
            return 


        for task in task_list: 

            if task.parent_id: continue # we don't want subtasks for now

            # this can (and probably should) be made into a function
            task_id = task.id
            description = task.description
            string_date = task.due.string # date you should've complete the task as a string


            lines = description.split('\n')
            # Fetch information from the task 
            book = lines[0][6:] #str
            author = lines[1][8:] #str
            chapter = lines[2][9:] #str
            review_number = int(lines[3][15:]) #int
            priority = int(lines[4][10: ]) # int
            code = lines[5][6:] # str
            original_date = datetime.datetime.strptime(lines[6][15:], date_format).date()

            problem_subset = []

            # Now we collect all problems associated with the task
            for subtask in task_list:
                if subtask.parent_id == task_id:
                    problem_subset.append(subtask.content)


            
            #store in database
            # can be made into a function as well
            with shelve.open('database\\database', writeback=False) as db:
                if code in db:
                    topic_obj = db[code]
                    review_obj = Review(problem_subset=problem_subset, topic=topic_obj, original_date=original_date, review_number=review_number)
                    count += 1
                    number_of_days = (today - datetime.datetime.strptime(string_date, r'%d/%m/%Y').date()).days # how many days is this task overdue?
                    topic_obj.update_reviews_date(number_of_days=number_of_days)
                    review_obj.new_date(today)
                    topic_obj.reviews.insert(0, review_obj)
                    db[code] = topic_obj

                else:
                    pass # ToDo

            self.api.close_task(task_id) #closes task only if it has succesfully returned to database

        print(f'{count} reviews were sucessfully returned to the database.')



    def send_reviews_from_database(self):

        last_access = metadata_manager.last_access_date()

        if last_access == today:
                print('Today\'s reviews have already been sent to Todoist.')
                return None
        
        today_reviews = []

        #makes a backup of database before attempting to send reviews to Todoist
        backup_database()

        with shelve.open('database\\database', writeback=False) as db:
            for code in db:
                topic_obj = db[code]

                if topic_obj.reviews[0].review_date <= today:
                    review = topic_obj.pop_review()
                    number_of_days = (today - review.review_date).days
                    # print('number_of_days =', number_of_days)
                    topic_obj.update_reviews_date(number_of_days=number_of_days)
                    review.new_date(today)
                    today_reviews.append(review)

                if not topic_obj.reviews: # There are no more reviews of the topic
                    del db[code]
                
                db[code] = topic_obj
                    
            today_reviews.sort(reverse=True) #sort by priority

            for review_obj in today_reviews[:configurations.daily_limit]:
                try:
                    self.add_review(review_obj)
                except Exception as E:
                    print(f'{today}',E, file=open('error_log.txt', 'a'))
                    print('Couldn\'t send one or more reviews to Todoist, possibly due to a Todoist internal error.')
                    print('It is recommended that you use the most recent backup of the database, ', end='')
                    print('delete any review currently in Todoist and try again later.')
                    return 

            for review_obj in today_reviews[configurations.daily_limit:]:
                code = review_obj.topic.code

                if code in db:
                    topic_obj = db[code]
                    topic_obj.reviews.insert(0, review_obj)
                    topic_obj.update_reviews_date(number_of_days=1)

                    db[code] = topic_obj
                else:
                    print('Code is not in database.')
                    pass #ToDo

        metadata_manager.update_last_access_date()



   




        



        



            
            


            
            









