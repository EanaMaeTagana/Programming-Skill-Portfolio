from tkinter import *
from tkinter import filedialog, messagebox

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

""" 
WIDGETS ADDED FOR EXTENDED TASK
"""
sort_ascending_btn = Button(root, text="Sort (Ascending)", width=30, command=lambda: [readStudentRecords(), sortAscending()])
sort_ascending_btn.grid(row=4, column=0, padx=5, pady=5)

sort_descending_btn = Button(root, text="Sort (Descending)", width=30, command=lambda: [readStudentRecords(), sortDescending()])
sort_descending_btn.grid(row=4, column=1, padx=5, pady=5)

update_record_btn = Button(root, text="Update Student Record", width=30, command=lambda: updateStudentRecord())
update_record_btn.grid(row=4, column=2, padx=5, pady=5)

add_record_btn = Button(root, text="Add Student Record", width=30, command= lambda: addStudentRecord())
add_record_btn.grid(row=5, column=0, padx=5, pady=5)

delete_record_btn = Button(root, text="Delete Student Record", width=30, command=lambda: deleteStudentRecord())
delete_record_btn.grid(row=5, column=1, padx=5, pady=5)

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

""" 
FUNCTIONS FOR EXTENDED TASK
"""

""" 
sortAscending(): 
- sorts the student records in ascending order based on student names
"""
def sortAscending():
    global student_records # accesses the global records
    student_records.sort(key=lambda x: x['Students Name']) # sorts records asceding-wise according to 'Students Name' within the tuple list
    allStudents() # calls the function to display all records

""" 
sortDescending(): 
- sorts the student records in descending order based on student names
"""
def sortDescending():
    global student_records # accesses the global records
    student_records.sort(key=lambda x: x['Students Name'], reverse=True) # sorts records descending-wise according to 'Students Name' within the tuple list
    allStudents() # calls the function to display all records

""" 
addStudentRecord()
- creates a window in which the user can input new student records
"""
def addStudentRecord():

    # function which takes the user input and saves the records
    def saveRecord(): 

        # gets the input values from the entry fields and removes all the white space
        student_id = id_entry.get().strip()
        student_name = name_entry.get().strip() 
        coursework1 = coursework1_entry.get().strip()
        coursework2 = coursework2_entry.get().strip()
        coursework3 = coursework3_entry.get().strip()
        exam_mark = exam_entry.get().strip()

        # checks if all fields have an input, if not, shows an error message
        if not all([student_id, student_name, coursework1, coursework2, coursework3, exam_mark]):
            messagebox.showerror("Error", "Invalid. Please fill in all fields.")
            return
        
        # block of code which executes when all fields have an input
        try:
            # converts the following input value into an integer
            student_id = int(student_id)
            coursework1 = int(coursework1)
            coursework2 = int(coursework2)
            coursework3 = int(coursework3)
            exam_mark = int(exam_mark)

            # validates if all coursework scores are 0-20
            if any(score < 0 or score > 20 for score in [coursework1, coursework2, coursework3]):
                messagebox.showerror("Error", "Coursework scores must be between 0 and 20.")
                return

            # validates if exam scores are 0-100
            if exam_mark < 0 or exam_mark > 100:
                messagebox.showerror("Error", "Exam mark must be between 0 and 100.")
                return

            current_count = 0 # initializes the count for the student record

            # reads the current record count from the file, else shows an error message
            try:
                with open("studentMarksExtension.txt", "r") as file:
                    lines = file.readlines()
                    current_count = int(lines[0].strip())
            except FileNotFoundError:
                messagebox.showerror("Error", "Student records file not found. Initializing a new file.")
            
            new_count = current_count + 1 # increments the student count

            # writes the updated student count and the student record input from the user into the text file
            with open("studentMarksExtension.txt", "w") as file:
                file.write(f"{new_count}\n")
                if current_count > 0:
                    file.writelines(lines[1:]) # keeps the existing records
                file.write(f"\n{student_id},{student_name},{coursework1},{coursework2},{coursework3},{exam_mark}")

            # closes the add record window then updates the list
            add_window.destroy()  
            readStudentRecords()  
            allStudents()        

        # error shown if invalid values are entered
        except ValueError:
            messagebox.showerror("Error", "Please enter valid integer values for ID and marks.")

    # creates a window to add new student records
    add_window = Toplevel(root)
    add_window.title("Add Student Record")
    add_window.configure(bg="#e8f6ff")

    # ui widgets (labels and entries) for add student window
    id_label = Label(add_window, text="Student ID:", bg="#e8f6ff")
    id_label.grid(row=0, column=0, pady=5)
    id_entry = Entry(add_window)
    id_entry.grid(row=0, column=1, pady=5)

    name_label = Label(add_window, text="Student Name:", bg="#e8f6ff")
    name_label.grid(row=1, column=0, pady=5)
    name_entry = Entry(add_window)
    name_entry.grid(row=1, column=1, pady=5)

    coursework1_label = Label(add_window, text="Coursework 1:", bg="#e8f6ff")
    coursework1_label.grid(row=2, column=0, pady=5)
    coursework1_entry = Entry(add_window)
    coursework1_entry.grid(row=2, column=1, pady=5)

    coursework2_label = Label(add_window, text="Coursework 2:", bg="#e8f6ff")
    coursework2_label.grid(row=3, column=0, pady=5)
    coursework2_entry = Entry(add_window)
    coursework2_entry.grid(row=3, column=1, pady=5)

    coursework3_label = Label(add_window, text="Coursework 3:", bg="#e8f6ff")
    coursework3_label.grid(row=4, column=0, pady=5)
    coursework3_entry = Entry(add_window)
    coursework3_entry.grid(row=4, column=1, pady=5)

    exam_label = Label(add_window, text="Exam Mark:", bg="#e8f6ff")
    exam_label.grid(row=5, column=0, pady=5)
    exam_entry = Entry(add_window)
    exam_entry.grid(row=5, column=1, pady=5)

    # button to save record which triggers the saveRecord() function
    save_btn = Button(add_window, text="Save Record", command=saveRecord)
    save_btn.grid(row=6, columnspan=2, pady=5)

""" 
deleteStudentRecord()
- creates a window in which the user can delete a student record by entering the student id
"""
def deleteStudentRecord():

    # function which takes the user input and deletes the records
    def confirmDelete():

        # gets the user input from the entry field and removes any white space
        student_id = delete_id_entry.get().strip() 
        
        # checks if the field is left blank, displays an error message if left blank
        if not student_id:
            messagebox.showerror("Error", "Invalid. Please enter a student ID")
            return
        
        found = False # checks if student record was found
        updated_records = [] # stores updated record
        
        # reads and stores current records
        with open("studentMarksExtension.txt", "r") as file:
            lines = file.readlines()
            current_count = int(lines[0].strip())  

        # rewrites the student record, skipping over the record to delete
        with open("studentMarksExtension.txt", "w") as file:
            file.write(f"{current_count}\n")  
            # iterates over each line within the file to check if it matches the id inputed by the user
            for line in lines[1:]: 
                if line.strip().split(',')[0] != student_id: # if it does NOT match, it will write the line
                    file.write(line)
                else: # if it matches, marks as found
                    found = True
        
        # if student record was found, displays a message indicating that the task wask completed
        if found:
            messagebox.showinfo("Success", f"Student with ID {student_id} has been deleted")
            delete_window.destroy() # closes the input student id window
            readStudentRecords() # refreshes the records
            allStudents() # displays new set of records
            
            # updates the new student count
            new_count = current_count - 1

            # edits the number of students at the beginning of the text file, indicating the new number of students
            with open("studentMarksExtension.txt", "r+") as file:
                lines = file.readlines()
                file.seek(0)  
                file.write(f"{new_count}\n")  
                file.writelines(lines[1:])  

        # error message if student id was not found
        else: 
            messagebox.showerror("Error", f"Sorry. No student found with ID {student_id}")

    # creates a window to delete student records
    delete_window = Toplevel(root)
    delete_window.title("Delete Student Record")
    delete_window.configure(bg="#e8f6ff")

    # ui widgets (labels and entries) for delete student window
    delete_id_label = Label(delete_window, text="Enter Student ID to delete:", bg="#e8f6ff")
    delete_id_label.grid(row=0, column=0, padx=5, pady=5)
    delete_id_entry = Entry(delete_window)
    delete_id_entry.grid(row=0, column=1, padx=5, pady=5)

    # button to delete record which triggers the confirmDelete() function
    delete_btn = Button(delete_window, text="Delete", command=confirmDelete)
    delete_btn.grid(row=1, columnspan=2, padx=5, pady=5)

""" 
updateStudentRecord()
- creates a window in which the user can update existing student records
- updates record by letting the user search the student by id or name, then updating by selecting a specific field
"""
def updateStudentRecord():

    # function which takes user input to update student records
    def saveUpdate():

        # gets the student to update either by id or name
        student_id = id_entry.get().strip()
        student_name = name_entry.get().strip()
        field_to_update = field_var.get()
        new_value = new_value_entry.get().strip()
        
        # checks to see if either a name or id was inputed, else shows an error message
        if not student_id and not student_name:
            messagebox.showerror("Error", "Please enter at least a Student ID or Name.")
            return
        
        found = False # checks to see if student record was found
        updated_records = []

        # reads the current record
        with open("studentMarksExtension.txt", "r") as file:
            lines = file.readlines()
            current_count = int(lines[0].strip()) # reads the total number of records
            
            # iterates over each record to check if a name or id matches the user input
            for line in lines[1:]:
                record_data = line.strip().split(',')
                if record_data[0] == student_id or record_data[1] == student_name:

                    found = True # updates as found
                    
                    # conditions which update the selected field, giving it a new value
                    if field_to_update == "Coursework 1":
                        record_data[2] = new_value
                    elif field_to_update == "Coursework 2":
                        record_data[3] = new_value
                    elif field_to_update == "Coursework 3":
                        record_data[4] = new_value
                    elif field_to_update == "Exam Mark":
                        record_data[5] = new_value

                    # updates the record, adding the new information
                    updated_records.append(','.join(record_data) + '\n')

                else:
                    updated_records.append(line)

        # writes the information within the file if id or name has a match
        if found:
            with open("studentMarksExtension.txt", "w") as file:
                file.write(f"{current_count}\n")  
                file.writelines(updated_records)  

            # informs the user that the task was completed 
            messagebox.showinfo("Success", "Student record updated successfully.")
            update_window.destroy() # closes the update record window
            readStudentRecords() # refreshes the records
            allStudents() # displays new set of records

        # error message if no matching id or name is found
        else: 
            messagebox.showerror("Error", "No matching student found.")

    # creates a window to update student record
    update_window = Toplevel(root)
    update_window.title("Update Student Record")
    update_window.configure(bg="#e8f6ff")

    # ui widgets (labels and entries) for update student record window
    id_label = Label(update_window, text="Student ID:", bg="#e8f6ff")
    id_label.grid(row=0, column=0, pady=5)
    id_entry = Entry(update_window, width=50)
    id_entry.grid(row=0, column=1, pady=5)

    name_label = Label(update_window, text="Student Name:", bg="#e8f6ff")
    name_label.grid(row=1, column=0, pady=5)
    name_entry = Entry(update_window, width=50)
    name_entry.grid(row=1, column=1, pady=5)

    field_label = Label(update_window, text="Field to update:", bg="#e8f6ff")
    field_label.grid(row=2, column=0, pady=5)
    
    # variable and radiobuttons in which the user selects the data to update
    field_var = StringVar(value="Coursework 1")  
    fields = ["Coursework 1", "Coursework 2", "Coursework 3", "Exam Mark"]
    
    field_label = Label(update_window, text="Field to update:", bg="#e8f6ff")
    field_label.grid(row=2, column=0, pady=5)

    field_frame = Frame(update_window, bg="#e8f6ff")
    field_frame.grid(row=2, column=1, columnspan=3, pady=5)

    fields = ["Coursework 1", "Coursework 2", "Coursework 3", "Exam Mark"]
    for field in fields:
        Radiobutton(field_frame, text=field, variable=field_var, value=field, bg="#e8f6ff").pack(side=LEFT)

    # entries in which the new data will be inputed
    new_value_label = Label(update_window, text="New Value:", bg="#e8f6ff")
    new_value_label.grid(row=3, column=0, pady=5)
    new_value_entry = Entry(update_window, width=50)
    new_value_entry.grid(row=3, column=1, pady=5)

    # button to save the new record and trigger the saveUpdate() function
    save_btn = Button(update_window, text="Update Record", command=saveUpdate)
    save_btn.grid(row=4, columnspan=2, pady=5)

root.mainloop()