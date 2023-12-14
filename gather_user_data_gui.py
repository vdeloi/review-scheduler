import tkinter as tk
from tkinter import ttk, messagebox

def gather_data():
    data = {'problem_set': []}

    def add_exercises():
        prefix = prefix_entry.get()
        exercise_range = exercise_range_entry.get().split('-')

        if len(exercise_range) == 1:
            lower_range = 1
            upper_range = int(exercise_range[0])
        else:
            lower_range = int(exercise_range[0])
            upper_range = int(exercise_range[-1])

        exercises = [prefix + str(i) for i in range(lower_range, upper_range + 1)]
        data['problem_set'].extend(exercises)

        # Show confirmation message
        message = f"Exercise set added: {', '.join(exercises)}"
        messagebox.showinfo("Confirmation", message)

    def finish_data_gathering():
        data['book'] = book_name_entry.get()
        data['author'] = author_name_entry.get()
        data['chapter'] = chapter_name_entry.get()
        data['priority'] = int(priority_var.get())  # New line for priority note that priority is an int
        root.destroy()

    root = tk.Tk()
    root.title("Data Gathering GUI")

    main_frame = ttk.Frame(root, padding="10")
    main_frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    # Book Information Frame
    book_frame = ttk.LabelFrame(main_frame, text="Book Information")
    book_frame.grid(column=0, row=0, padx=10, pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))

    ttk.Label(book_frame, text="Book Name:").grid(column=0, row=0, sticky=tk.W)
    book_name_entry = ttk.Entry(book_frame)
    book_name_entry.grid(column=1, row=0, sticky=(tk.W, tk.E))

    ttk.Label(book_frame, text="Author Name:").grid(column=0, row=1, sticky=tk.W)
    author_name_entry = ttk.Entry(book_frame)
    author_name_entry.grid(column=1, row=1, sticky=(tk.W, tk.E))

    ttk.Label(book_frame, text="Chapter Name/Number:").grid(column=0, row=2, sticky=tk.W)
    chapter_name_entry = ttk.Entry(book_frame)
    chapter_name_entry.grid(column=1, row=2, sticky=(tk.W, tk.E))

    # New Entry for Priority
    ttk.Label(book_frame, text="Priority Level (0-2):").grid(column=0, row=3, sticky=tk.W)
    priority_var = tk.StringVar(value="0")  # Default value is 0
    priority_entry = ttk.Combobox(book_frame, textvariable=priority_var, values=["0", "1", "2"])
    priority_entry.grid(column=1, row=3, sticky=(tk.W, tk.E))

    # Exercises Information Frame
    exercises_frame = ttk.LabelFrame(main_frame, text="Exercises Information")
    exercises_frame.grid(column=0, row=1, padx=10, pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))

    ttk.Label(exercises_frame, text="Prefix:").grid(column=0, row=0, sticky=tk.W)
    prefix_entry = ttk.Entry(exercises_frame)
    prefix_entry.grid(column=1, row=0, sticky=(tk.W, tk.E))

    ttk.Label(exercises_frame, text="Exercise Range:").grid(column=0, row=1, sticky=tk.W)
    exercise_range_entry = ttk.Entry(exercises_frame)
    exercise_range_entry.grid(column=1, row=1, sticky=(tk.W, tk.E))

    ttk.Button(exercises_frame, text="Add Exercises", command=add_exercises).grid(column=0, row=2, columnspan=2)

    # Finish Button
    ttk.Button(main_frame, text="Finish", command=finish_data_gathering).grid(column=0, row=2, pady=10)

    root.mainloop()

    return data

if __name__ == '__main__':
    try:
        data = gather_data()
        print(data)
        print("Ok")
        input()
    except Exception as e:
        print(e, file=open("error log.txt", 'w'))
