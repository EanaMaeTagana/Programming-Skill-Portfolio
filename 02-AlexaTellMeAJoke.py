from tkinter import *
import random

# functions create the main window and sets the title, size, and background color
root = Tk()
root.title("Alexa Tell Me A Joke")
root.geometry("500x400")
root.resizable(0, 0)
root.configure(bg="#995349")

""" 
displayMenu(): 
- reads the joke from the file and returns the a list of tuples containing a setup of a joke and a punchline
"""
def readJoke():
    with open("joke.txt") as joke_handler, open("punchline.txt") as punchline_handler: # opens the files 
        # declares variables for the files and reads the lines
        jokes = joke_handler.readlines() 
        punchlines = punchline_handler.readlines()
        joke_pairs = list(zip(jokes, punchlines)) # pairs the jokes with their punchlines
        return [(setup.strip(), punchline.strip()) for setup, punchline in joke_pairs]

# variables declared 
random_joke = readJoke() # sets random_joke variable as the one read from readJoke() function
current_joke = None # holds the joke to be displayed

""" 
displayJoke():
- chooses a random joke and display setup then displays on the window
"""
def displayJoke():
    global current_joke 
    if random_joke:
        current_joke = random.choice(random_joke) # selects a random joke from the list of tuples
        joke_label.config(text=current_joke[0]) # displays the joke setup
        punchline_label.config(text="") # clears the previous punchline, if needed 
        punchline_btn.config(state=NORMAL) # enables the punchline button
    else:
        joke_label.config(text="No jokes found!") # error handling if no jokes

"""
displayPunchline():
- displays the punchline of the current joke
"""
def displayPunchline():
    if current_joke:
        punchline_label.config(text=current_joke[1]) # shows the punchline

"""
quitProgram():
- closes the application window.
"""
def quitProgram():
    root.destroy() # destroys the window, ending the program

# ui widgets using tkinter to display the jokes and buttons

title = Label(root, text="Alexa, tell me a joke!", wraplength=400, bg="#995349", fg="#ffffff", font=("Comic Sans MS", 40), anchor="n")
title.place(x=50, y=20, width=400)

joke_label = Label(root, wraplength=400, bg="#995349", fg="#ffffff", font=("Comic Sans MS", 25), anchor="n")
joke_label.place(x=50, y=110, height=100, width=400)

punchline_label = Label(root, wraplength=400, bg="#995349", fg="#ffffff", font=("Comic Sans MS", 18), anchor="n")
punchline_label.place(x=50, y=210, height=55, width=400)

# button to display joke
joke_btn = Button(root, text="Alexa, tell me a joke", command=displayJoke, bg="#1b6ba8", fg="#000000", font=("Comic Sans MS", 15))
joke_btn.place(x=50, y=300, width=195)

# button to display punchline
punchline_btn = Button(root, text="Tell me the punchline", command=displayPunchline, state=DISABLED, font=("Comic Sans MS", 15))
punchline_btn.place(x=255, y=300, width=195)

# button to end program
quit_btn = Button(root, text="Quit", command=quitProgram, bg="#ff4d4d", fg="#000000", font=("Comic Sans MS", 15))
quit_btn.place(x=50, y=340, width=400)

root.mainloop()