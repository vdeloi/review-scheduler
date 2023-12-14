# data_gathering.py

def data_gathering():
    print("***Book information***")
    book_name = input("Enter the book name: ")
    author_name = input("Enter the author name: ")
    chapter_name = input("Enter the chapter number and/or name: ")

    print("***Exercises information***")

    exercises = []

    while True:
        prefix = input("Enter the prefix of the exercise if it has one: ")
        exercise_range = input(
'''Enter the range of the number of exercises separated by a dash
example: type 26-82 to include the exercises 26, 27, ... 82.''').split('-')
        
        if len(exercise_range) == 1:
            lower_range = 1
            upper_range = int(exercise_range[0])

        else:
            lower_range = int(exercise_range[0])
            upper_range = int(exercise_range[-1])
        
        exercises += [prefix + str(i) for i in range(lower_range, upper_range + 1)]

        ans = input("Would you like to add another set of exercises [y/n]: ")

        if ans.lower() == 'n':
            break 

    return dict(
        [
            ('book', book_name),
            ('author', author_name),
            ('chapter', chapter_name),
            ('exercises', exercises)]
        )
        

if __name__ == '__main__':
    try:
     print(data_gathering())
     print("Ok")
     input()
    except Exception as E:
        print(E, file=open("error log.txt", 'w'))
        
