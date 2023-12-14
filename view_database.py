import shelve
import datetime
from date_provider import date_format


today = datetime.date.today()



filename = 'database\\database'

print(today)

with shelve.open(filename) as db:

    for code in db:
        topic_obj = db[code]
        
        print('Code: ', topic_obj.code)
        print('Book: ', topic_obj.book)
        print('Author: ', topic_obj.author)
        print('Chapter: ', topic_obj.chapter)

        for review_obj in topic_obj.reviews:
            print(
                '     Review number: ', 
                review_obj.review_number,
                ' ' ,
                'Review date: ', 
                review_obj.review_date.strftime(date_format), 
                'Number of problems:', len(review_obj.problem_subset)
                )

        print()



input("Type anything to exit.")
    

    

