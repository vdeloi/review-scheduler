# configurations.py

# original [1, 3, 7, 11, 22, 44, 88, 176, 352, 704]
review_intervals = [1, 3, 7, 9, 11, 22, 33, 44, 66, 88, 176, 352, 528, 704]  # t0 + interval
number_of_reviews = len(review_intervals)
daily_limit = 5 # Maximum number of reviews sent to Todoist in a day

# Todoist 
project_id =  # reviews project
api_token =  