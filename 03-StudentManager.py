from tkinter import *
from tkinter import filedialog

# functions create the main window and sets the title, size, and background color
root=Tk()
root.title("Student Manager")
root.resizable(0, 0)
root.configure(bg="#e8f6ff")

# variable declared before functions
user_input = StringVar()

# sets the main window and ui widgets
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

menu_title = Label(root, text="Student Manager", bg="#e8f6ff", font=("Arial", 32))
menu_title.grid(row=0, column=0, columnspan=4, pady=25)

# buttons which trigger specific functions
view_all_btn = Button(root, text="View All Student Records", width=30, command=lambda: [readStudentRecords(), allStudents()])
view_all_btn.grid(row=1, column=0, padx=5, pady=5)

highest_score_btn = Button(root, text="Show Highest Score", width=30, command=lambda: [readStudentRecords(), highestStudentScore()])
highest_score_btn.grid(row=1, column=1, padx=5, pady=5)

lowest_score_btn = Button(root, text="Show Lowest Score", width=30, command=lambda: [readStudentRecords(), lowestStudentScore()])
lowest_score_btn.grid(row=1, column=2, padx=5, pady=5)

individual_score = Label(root, text="View Individual Student Record (ID):", bg="#e8f6ff", width=30)
individual_score.grid(row=2, column=0, padx=5, pady=5)

individual_score_btn = Button(root, text="View Record", width=30, command=lambda: [readStudentRecords(), individualStudentRecord()])
individual_score_btn.grid(row=2, column=2, padx=5, pady=5)

# entry field which takes user input
individual_score_entry = Entry(root, textvariable=user_input, width=30)
individual_score_entry.grid(row=2, column=1, padx=5, pady=5) 

# text area where information will be displayed
txtarea = Text(root, width=80, height=10)
txtarea.grid(row=3, column=0, columnspan=3, padx=5, pady=25)

# scroll bar function
scrollV = Scrollbar(root, orient="vertical", command=txtarea.yview)
scrollV.place(x=685, y=195, height=135)  

txtarea.config(yscrollcommand=scrollV.set)

student_records = [] # list to contain student records

""" 
readStudentRecords(): 
- reads student records from a text file, calculates total coursework and exam scores, overall percentage, and assigns grades then populates the list with the information
"""
def readStudentRecords():
    # declares global variables
    global student_records
    global total_students
    global class_average

    student_records = [] # clears the list
    all_scores = 0 # sets the scores to calculate class average
    
    # opens and reads the file for student data
    with open("studentMarks.txt") as file_handler:
        lines = file_handler.readlines() # reads all lines within the file

        # iterates through each line
        for line in lines:
            data = line.strip().split(',') # splits the lines by comma
            if len(data) == 6: # checks if each line has 6 fields, thus not reading the number of students line
                # sets the student data by index
                student_id = data[0]
                student_name = data[1]
                coursework_scores = [int(score) for score in data[2:5]]
                coursework_total = sum(coursework_scores) # calculates each student's coursework total
                exam_mark = int(data[5])
                total_score = coursework_total + exam_mark # calculates the overall score
                overall_percentage = (total_score / 160) * 100 # calculates the percentage
                
                # determines the grades according to the overall percentage
                if overall_percentage >= 70:
                    grade = 'A'
                elif overall_percentage >= 60:
                    grade = 'B'
                elif overall_percentage >= 50:
                    grade = 'C'
                elif overall_percentage >= 40:
                    grade = 'D'
                else:
                    grade = 'F'

                # creates a dictionary with student data
                student_record = {
                    'Students Number': student_id,
                    'Students Name': student_name,
                    'Total Coursework Mark': coursework_total,
                    'Exam Mark': exam_mark,
                    'Total Score': total_score,
                    'Overall Percentage': overall_percentage,
                    'Grade': grade
                }

                student_records.append(student_record) # adds the data to the student_record list

                all_scores += overall_percentage  # calculates the class percentage

    total_students = len(student_records) # sets the total of students as the count of records in student_records list
    class_average = all_scores / total_students if total_students > 0 else 0 # calculates class average if there are students; otherwise, sets it to 0
    return class_average # returns the class average

""" 
allStudents(): 
- takes the information from the readStudentRecords() function and displays all records
"""
def allStudents():
    txtarea.delete("1.0", "end") # clears the text area
    output = "" # initializes the output

    for record in student_records: # iterates through the list of records then sets the output as the given format
        output += ( 
            f"Students Name: {record['Students Name']}\n"
            f"Students Number: {record['Students Number']}\n"
            f"Total Coursework Mark: {record['Total Coursework Mark']}\n"
            f"Exam Mark: {record['Exam Mark']}\n"
            f"Overall Percentage: {record['Overall Percentage']:.2f}%\n"
            f"Grade: {record['Grade']}\n"
            f"{'-' * 25}\n"
        )

    output += ( # adds the total number of students then the class average
        f"Total Students: {total_students}\n"
        f"Average Percentage: {class_average}%\n"
    )

    txtarea.insert(END, output) # inserts the output into the text area

""" 
highestStudentScore(): 
- takes the information from the readStudentRecords() function and displays the student with the highest record
"""
def highestStudentScore():
    txtarea.delete("1.0", "end") # clears the text area

    highest_score = 0 # initializes the highest score to 0 to compare the scores
    top_student = None # placeholder to store students to compare
    output = "" # initializes the output

    for record in student_records: # iterates through the percentages everytime the percentage is less than the set score
        overall_score = record['Overall Percentage']  
        if overall_score > highest_score: # checks if score is bigger than highest_score
            highest_score = overall_score # sets the given score as overall_score 
            top_student = record # sets the top student as the current record

    if top_student: # if top student is found, sets the information in the following format
        output += (
            f"Students Name: {top_student['Students Name']}\n"
            f"Students Number: {top_student['Students Number']}\n"
            f"Total Coursework Mark: {top_student['Total Coursework Mark']}\n"
            f"Exam Mark: {top_student['Exam Mark']}\n"
            f"Overall Percentage: {top_student['Overall Percentage']:}%\n"
            f"Grade: {top_student['Grade']}\n"
        )
    else: # if no records are available
        output = "No student records found."

    txtarea.insert(END, output) # inserts the information into the text area

""" 
lowestStudentScore(): 
- takes the information from the readStudentRecords() function and displays the student with the lowest record
"""
def lowestStudentScore():
    txtarea.delete("1.0", "end") # clears the text area

    lowest_score = 100 # initializes the lowest score to 100 to compare the scores
    bottom_student = None # placeholder to store students to compare
    output = "" # initializes the output

    for record in student_records: # iterates through the percentages everytime the percentage is more than the set score
        overall_score = record['Overall Percentage']  
        if overall_score < lowest_score: # checks if score is less than lowest_score
            lowest_score = overall_score # sets the given score as overall_score 
            bottom_student = record # sets the top student as the current record

    if bottom_student: # if bottom student is found, sets the information in the following format
        output += (
            f"Students Name: {bottom_student['Students Name']}\n"
            f"Students Number: {bottom_student['Students Number']}\n"
            f"Total Coursework Mark: {bottom_student['Total Coursework Mark']}\n"
            f"Exam Mark: {bottom_student['Exam Mark']}\n"
            f"Overall Percentage: {bottom_student['Overall Percentage']:}%\n"
            f"Grade: {bottom_student['Grade']}\n"
        )
    else: # if no records are available
        output = "No student records found." 

    txtarea.insert(END, output) # inserts the information into the text area

""" 
individualStudentRecord(): 
- takes the information from the readStudentRecords() function and displays the student with as per the user input ID
"""
def individualStudentRecord():
    txtarea.delete("1.0", "end") # clears the text area

    input_ID = user_input.get() # takes the user input and sets it as the input_ID
    output = "" # initializes the output

    for record in student_records: # iterates through the student names to check if matching the user input
        student_ID = record['Students Number'] # checks if input matches a record
        if student_ID == input_ID: # if student is found, sets the information in the following format
            output += (
                f"Students Number: {record['Students Number']}\n"  
                f"Students Name: {record['Students Name']}\n"  
                f"Total Coursework Mark: {record['Total Coursework Mark']}\n"  
                f"Exam Mark: {record['Exam Mark']}\n"
                f"Overall Percentage: {record['Overall Percentage']:.2f}%\n"  
                f"Grade: {record['Grade']}\n"
            )
            break # ends the loop
    else: # if no record is found
        output = "No student record found with the given ID."

    txtarea.insert(END, output) # inserts the information into the text area

root.mainloop()