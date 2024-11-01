from tkinter import *
import random
import tkinter.messagebox

# functions create the main window and sets the title, size, and background color
root = Tk()
root.title("Mathematics Quiz")
root.geometry("450x350")
root.configure(bg="#e0f5ff")

# global variables declared to be used throughout the code
selected_level = IntVar(root)
answer = StringVar()
score = 0
correct = 0
question_count = 0
attempts = 0
menu_frame = None

# ui widgets using tkinter declared before being used within the dfunctions
border = Label(root, bg="#e0f5ff")
question = Label(root, text="", bg="#e0f5ff", font=("Tahoma", 35))
result = Label(root, text="", bg="#e0f5ff", font=("Tahoma", 35))
answer_entry = Entry(root, textvariable=answer, font=("Tahoma", 18))
submit_btn = Button(root, text="SUBMIT ANSWER", font=("Tahoma", 14))
reset_btn = Button(root, text="Play Again", command=lambda: resetQuiz(), font=("Tahoma", 14))

""" 
displayMenu(): 
- places the UI widgets within the main window and display the menu in which the level will be selected.
"""
def displayMenu():

# creates the menu and sets the widgets
    global menu_frame
    menu_frame = Frame(root, bg="#e0f5ff")  
    menu_frame.pack(expand=True)  

    menu_title = Label(menu_frame, text="MATHEMATICS QUIZ", bg="#e0f5ff", font=("Tahoma", 35))  
    menu_title.pack(pady=10)

    menu_difficulty = Label(menu_frame, text="SELECT A DIFFICULTY", bg="#e0f5ff", font=("Tahoma", 20)) 
    menu_difficulty.pack(pady=5)

# level difficulty radiobuttons
# when selected, sets the variable selected_level to a unique level (1=easy, 2=moderate, 3=advanced)
    easy_btn = Radiobutton(menu_frame, text="EASY", variable=selected_level, value=1, **default_style)
    easy_btn.pack(pady=10)
    moderate_btn = Radiobutton(menu_frame, text="MODERATE", variable=selected_level, value=2, **default_style)
    moderate_btn.pack(pady=10)
    advanced_btn = Radiobutton(menu_frame, text="ADVANCED", variable=selected_level, value=3, **default_style)
    advanced_btn.pack(pady=10)

# Enter difficulty button, triggers the startQuiz() function
    enter_difficulty_button = Button(menu_frame, text="BEGIN QUIZ", command=lambda: startQuiz(menu_frame), width=25)
    enter_difficulty_button.pack(pady=10)

""" 
startQuiz(): 
- verfies the selected level then sets up the quiz interface
"""
def startQuiz(menu_frame):

    # checks if a valid difficulty was selected, else shows an error message and exits the function
    if selected_level.get() not in [1, 2, 3]:
        tkinter.messagebox.showinfo("Invalid", "Invalid selection. Please select a valid difficulty level.")
        return
    
    # sets up the widgets of the quiz interface
    border.pack(pady=20) 
    menu_frame.pack_forget() # hides the menu frame to focus on the quiz interface
    question.pack(pady= 20)
    answer_entry.pack()  
    submit_btn.config(command=isCorrect) # sets the submit button, that when pressed calls the isCorrect() function
    submit_btn.pack(pady=20)  
    result.pack()  
    
    # calls the function displayProblem() to show the first question
    displayProblem() 

""" 
randomInt(): 
- generates the random values for each difficulty level
"""
def randomInt():

    # gets the value through the radiobuttons in the menu which sets the difficulty level (1=easy, 2=moderate, 3=advanced)
    difficulty = selected_level.get()

    # generates the numbers based on the difficulty level
    if difficulty == 1:
        # if 1=easy, generate two numbers between 1-9
        return random.randint(1, 9), random.randint(1, 9)
    elif difficulty == 2:
        # if 2=moderate, generate two numbers between 1-99
        return random.randint(1, 99), random.randint(1, 99)
    elif difficulty == 3:
        # if 3=advanced, generate two numbers between 1-9999
        return random.randint(1, 9999), random.randint(1, 9999)

""" 
randomInt(): 
- randomizes the operation to be used in the problem
"""
def decideOperation():
    
    # returns a random choice between add and subtract then returns the operation
    return random.choice(['+', '-'])

""" 
randomInt(): 
- displays the problem according to the generated number or randomized operation
- sets the correct answer based on the numbers and operation
- when the submit button is pressed after the answer the question, the isCorrect() function will be called
"""
def displayProblem():

    # variables declared before the function
    global correct, attempts # calls the global variables
    operation = decideOperation() # sets the operation as the one generated from the decideOperation() function
    num1, num2 = randomInt() # sets the numbers as the one generated from the randomInt() function

    # calculates and sets the answer of the generated question
    if operation == '+':
        correct = num1 + num2
    else:
        correct = num1 - num2

    # displays the question in the question
    question.config(text=f"What is {num1} {operation} {num2}?")

    # resets the attempts if a question is answered correctly
    attempts = 0  

""" 
isCorrect(): 
- verifies is the answer is correct
- gives points based on if question is answered on the first or second try
- generates a new question if correct, shows the question again for a second chance if incorrect
- displays the results if 10 questions have been answered
"""
def isCorrect():

    # variables declared before the function
    global score, question_count, attempts # calls the global variables
    user_answer = answer.get() # gets and sets the user_answer from the entry button

    # error handling code if user input is not a valid integer
    try:

        # condition when user answer is correct
        if int(user_answer) == correct: # checks if user answer matches the correct answer
            score += 10 if attempts == 0 else 5 # adds 10 points for the first attempt, 5 for second attempt
            tkinter.messagebox.showinfo("Correct", "Correct!") # displays a message stating that the users answer was correct
            answer.set("") # clears the entry field
            question_count += 1 # increases the question count
            attempts = 0 # resets the attempts to 0

        else:
            # when answer is incorrect and it is the first attempt 
            if attempts == 0:
                tkinter.messagebox.showinfo("Incorrect", "Incorrect! Try again.") # tells the user to try again 
                attempts += 1 # increases the attempt count
                answer.set("") # clears the entry field
                return # lets the user try again
            
            # when answer is incorrect and it is the second attempt 
            else:
                tkinter.messagebox.showinfo("Incorrect", f"Incorrect! The correct answer was {correct}.") # tells the user that the answer was wrong and of the right answer
                answer.set("") # clears the entry field
                question_count += 1 # increases the question count
                attempts = 0 # resets the attempts to 0
        
        # checks if the user has answered 10 questions 
        if question_count < 10: 
            displayProblem() # if less than 10, display a new question
        else:
            displayResults() # if more than 10, resets for a new quiz if needed
            attempts = 0

    # shows error message when invalid input
    except ValueError: 
        tkinter.messagebox.showerror("Invalid input", "Please enter a valid number.")

""" 
displayResults(): 
- displays the results according to the amount of points then displays a message of the grade
"""
def displayResults():
    check_score = score  
    if check_score >= 90:
        result.config(text="Your score is A+!")
    elif check_score >= 80:
        result.config(text="Your score is A-!")
    elif check_score >= 70:
        result.config(text="Your score is B+!")
    elif check_score >= 60:
        result.config(text="Your score is B-!")
    elif check_score >= 50:
        result.config(text="Your score is C+!")
    elif check_score >= 40:
        result.config(text="Your score is C-!")
    elif check_score >= 30:
        result.config(text="Your score is D!")
    else:
        result.config(text="Sorry! You failed.")
    
    # widgets to restart quiz
    answer_entry.pack_forget()
    question.pack_forget()
    submit_btn.pack_forget()
    reset_btn.pack(pady=20)  

""" 
resetQuiz(): 
- resets the quiz and resets the variables and entries
"""
def resetQuiz():
    global score, question_count, correct
    score = 0
    question_count = 0
    correct = 0
    result.config(text="")
    answer.set("")
    reset_btn.pack_forget()  
    displayMenu() # calls the displayMenu() to restart quiz and allow the user to pick a different difficulty

# sets a default style to the radiobuttons
default_style = {
    'font': ("Tahoma", 14),
    'bg': "#e0f5ff", 
}

# calls the displayMenu() function to display the menu interface
displayMenu()

root.mainloop()