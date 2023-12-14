# models.py

import random
import datetime
import configurations
from date_provider import date_format

today = datetime.date.today()


class Topic:
    
    def __init__(self, book, author, chapter, problem_set, code, priority=0):
        self.book = book
        self.author = author
        self.chapter = chapter
        self.problem_set = problem_set
        self.code = None
        self.reviews = []
        self.subsets = [] # this list is storing the subset of problems of all reviews 
        self.priority = priority
        self.code = code

    def split_problem_set(self):

        random.shuffle(self.problem_set)
        problem_set_length = len(self.problem_set)
            
        for i in range(configurations.number_of_reviews):
            tmp = []

            for j in range( problem_set_length // configurations.number_of_reviews ):
                a = self.problem_set.pop(0)
                tmp.append(a)
            self.subsets.append(tmp)
            

        # The remaining problems
        for i, problem in enumerate(self.problem_set):
            self.subsets[i].append(problem)


    def update_reviews_date(self, number_of_days):
        for review in self.reviews:
            review.update_date(number_of_days)
        

    def create_review_objects(self):

        self.split_problem_set()
        
        for i in range(configurations.number_of_reviews):
            problem_subset = self.subsets[i]
            original_date = today + datetime.timedelta(days=configurations.review_intervals[i])
            review_number = i + 1
            topic = self

            self.reviews.append(Review(problem_subset, original_date, review_number, topic))

    def delete_problem(self, problem_to_delete):
        
        for review in self.reviews:
            if problem_to_delete in review.problem_subset:
                review.problem_subset.remove(problem_to_delete)
                print('Problem sucessfully deleted.')
                break
        else:
            print("Couldn't find the problem.")

    def pop_review(self):
        review = self.reviews.pop(0)
        return review



    


class Review:
    
    def __init__(self, problem_subset, original_date, review_number, topic):
        self.problem_subset = problem_subset
        self.original_date = original_date
        self.review_number = review_number
        self.topic = topic
        self.review_date = self.original_date

    def update_date(self, number_of_days):
        self.review_date = self.review_date + datetime.timedelta(days=number_of_days)

    def new_date(self, new_date):
        self.review_date = new_date

    def __gt__(self, other): # reviewA > reviewB means reviewA is more important than reviewB
        if self.topic.priority > other.topic.priority:
            return True
        elif self.topic.priority == other.topic.priority:
            if self.review_number < other.review_number:
                return True
            elif self.review_number == other.review_number:
                if self.original_date < other.original_date:
                    return True
                else:
                    return False 
            else:
                return False
        else:
            return False
        
    def description(self):
                return (
f'''Book: {self.topic.book}
Author: {self.topic.author}
Chapter: {self.topic.chapter}
Review number: {self.review_number}
Priority: {self.topic.priority}
Code: {self.topic.code}
Original date: {self.original_date.strftime(date_format)}''')
    
    def content(self):
        return f'{self.topic.book} - {self.topic.chapter}'


