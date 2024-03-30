import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"

class Task:
    def __init__(self, username = None, title = None, description = None, due_date = None, assigned_date = None, completed = None):
        '''
        Inputs:
        username: String
        title: String
        description: String
        due_date: DateTime
        assigned_date: DateTime
        completed: Boolean
        '''
        self.username = username
        self.title = title
        self.description = description
        self.due_date = due_date
        self.assigned_date = assigned_date
        self.completed = completed

    def from_string(self, task_str):
        '''
        Convert from string in tasks.txt to object
        '''
        tasks = task_str.split(";")
        username = tasks[0]
        title = tasks[1]
        description = tasks[2]
        due_date = datetime.strptime(tasks[3], DATETIME_STRING_FORMAT)
        assigned_date = datetime.strptime(tasks[4], DATETIME_STRING_FORMAT)
        completed = True if tasks[5] == "Yes" else False
        self.__init__(username, title, description, due_date, assigned_date, completed)


    def to_string(self):
        '''
        Convert to string for storage in tasks.txt
        '''
        str_attrs = [
            self.username,
            self.title,
            self.description,
            self.due_date.strftime(DATETIME_STRING_FORMAT),
            self.assigned_date.strftime(DATETIME_STRING_FORMAT),
            "Yes" if self.completed else "No"
        ]
        return ";".join(str_attrs)

    def display(self):
        '''
        Display object in readable format
        '''
        disp_str = f"Task: \t\t {self.title}\n"
        disp_str += f"Assigned to: \t {self.username}\n"
        disp_str += f"Date Assigned: \t {self.assigned_date.strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Due Date: \t {self.due_date.strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Task Description: \n {self.description}\n"
        return disp_str

def readTasks(file):
    """
    Functions to read the text file containing task info
    Converts task info into a task object
    Generates list of task objects

    file: string -> name of file containing tasks
    """
    # Read and parse tasks.txt
    if not os.path.exists(file):
        with open(file, "w") as default_file:
            pass

    #Gets info of a task and generates a list of task info
    with open(file, 'r') as task_file:
        task_data = task_file.read().split("\n")
        task_data = [t for t in task_data if t != ""]

    #Converts task info into a task object
    task_list = []
    for t_str in task_data:
        curr_t = Task()
        curr_t.from_string(t_str)
        task_list.append(curr_t)
    
    return task_list

def readUsers(file):
    """
    Function to read all the users and passwords in a text file
    Writes and admin user if no users exist
    Puts user and respective passwords into a dict

    file: string -> name of file containing users and passwords
    """
    # If no user.txt file, write one with a default account
    if not os.path.exists(file):
        with open(file, "w") as default_file:
            default_file.write("admin;password")

    # Read in user_data
    with open(file, 'r') as user_file:
        user_data = user_file.read().split("\n")

    # Convert to a dictionary
    username_passwords = {}
    for user in user_data:
        username, password = user.split(';')
        username_passwords[username] = password
    
    return username_passwords

def login(usernames):
    """
    Function that asks for a login username and password until a valid user and password is given

    usernames: dict -> Containing all usernames and passwords
    """
    logged_in = False
    while not logged_in:

        print("LOGIN")
        curr_user = input("Username: ")
        curr_pass = input("Password: ")
        if curr_user not in usernames.keys():
            print("User does not exist")
            continue
        elif usernames[curr_user] != curr_pass:
            print("Wrong password")
            continue
        else:
            print("Login Successful!")
            logged_in = True
            return curr_user        

def validate_string(input_str):
    '''
    Function for ensuring that string is safe to store
    '''
    if ";" in input_str:
        print("Your input cannot contain a ';' character")
        return False
    return True

def check_username_and_password(username, password):
    '''
    Ensures that usernames and passwords can't break the system
    '''
    # ';' character cannot be in the username or password
    if ";" in username or ";" in password:
        print("Username or password cannot contain ';'.")
        return False
    return True

def write_usernames_to_file(username_dict):
    '''
    Function to write username to file

    Input: dictionary of username-password key-value pairs
    '''
    with open("user.txt", "w") as out_file:
        user_data = []
        for k in username_dict:
            user_data.append(f"{k};{username_dict[k]}")
        out_file.write("\n".join(user_data))

def check_user(exist = 1):
    """
    Checks if a user exists or does not exist and asks to enter another name
    exist = 0 -> Checks for existing users
    exist != 0 -> Checks for non-existing users
    """
    #Loops until a valid user is given
    while True:
        new_username = input("Username: ")
        
        if exist == 0:
            if new_username not in username_passwords.keys():
                break
            print("User already exists. Please enter a new user.")
        else:
            if new_username in username_passwords.keys():
                break
            print("User does not exist. Please enter an existing user.")
    return new_username

def date_input():
    # Obtain and parse due date
    while True:
        try:
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            return due_date_time
        except ValueError:
            print("Invalid datetime format. Please use the format specified")

def write_task():
    # Write to tasks.txt
    with open("tasks.txt", "w") as task_file:
        task_file.write("\n".join([t.to_string() for t in task_list]))
    print("Task successfully added.")

def reg_user():
    """
    Function to register a new user

    Checks for valid formatting for username and password
    Confirms password
    """
    print("Please enter a new username")
    #Checks for existing users
    new_username = check_user(0)

    #User input new password
    new_password = input("New Password: ")

    #Checks inputs don't have a ; in them
    if not check_username_and_password(new_username,new_password):
        return False
    
    confirm_password = input("Confirm Password: ")

    # Check if the new password and confirmed password are the same.
    if new_password == confirm_password:
        # If they are the same, add them to the user.txt file,
        print("New user added")

        # Add to dictionary and write to file
        username_passwords[new_username] = new_password
        write_usernames_to_file(username_passwords)

    # Otherwise you present a relevant message.
    else:
        print("Passwords do no match")


def add_task():
    """
    Function to allow users to add tasks for other existing users
    """
    #Checks for non-existing users
    print("Please assign the task to a user")
    task_username = check_user()


    # Get title of task and ensure safe for storage
    while True:
        task_title = input("Title of Task: ")
        if validate_string(task_title):
            break

    # Get description of task and ensure safe for storage
    while True:
        task_description = input("Description of Task: ")
        if validate_string(task_description):
            break


    due_date_time = date_input()

    # Obtain and parse current date
    curr_date = date.today()
    
    # Create a new Task object and append to list of tasks
    new_task = Task(task_username, task_title, task_description, due_date_time,curr_date, False)
    task_list.append(new_task)

    write_task()

def view_all():
    """
    Function is display all tasks on the system
    """
    print("-----------------------------------")

    if len(task_list) == 0:
        print("There are no tasks.")
        print("-----------------------------------")

    for t in task_list:
        print(t.display())
        print("-----------------------------------")

def view_mine():
    """
    Function to display a list of tasks assigned to current user
    Allows user to expand a chosen task for more information
    Allows user to set task as complete
    Allows user to edit assigned user or due date of task
    """
    print("-----------------------------------")
    #Tag delaring if user has any tasks
    has_task = False

    #Task counter
    task_number = 1

    #Declaring list that will cotain task objects of a user
    user_tasks = []
    
    #Loops through all tasks in the system
    for t in task_list:
        #Checks if task is assigned to the current user
        if t.username == curr_user:
            has_task = True
            
            #Prints out all tasks belonging to current user
            print(f"{task_number}: {t.title}")
            
            #Increase the task number
            task_number += 1

            #Update the task list
            user_tasks.append(t)
    print("-----------------------------------")        
    print("Please select which task to open. enter -1 to go back to the menu.")
    
    #User selects a task to expand

    selection = int(input("Selection: "))
    #Back out if the user wants to go back to the main menu
    if selection == -1:
        return

    #Expands selected task
    curr_task = user_tasks[selection-1]
    print(curr_task.display())
    print("-----------------------------------")

    #User selects if they want to mark as complete or edit the task
    print("1: Mark as complete")
    print("2: Edit incomplete task")
    tick_edit = int(input("Selection: "))

    #Gets if the task is completed
    completed = curr_task.completed
    
    #User wants to complete the task
    if tick_edit == 1:
        curr_task.completed = "Yes"

        #Update task file
        write_task()

        print("Task completed")
        print("-----------------------------------")

    #User wants to edit the task, that is NOT completed
    elif tick_edit == 2 and not completed:
        
        #User selects which part of the task they want to edit
        print("1: Assigned user")
        print("2: Due date")
        edit = int(input("Selection: "))

        #User wants to edit the assigned user
        if edit == 1:

            #Check is user exists
            new_user = check_user()

            #Edit assinged user
            curr_task.username = new_user
            
            #Update task file
            write_task()
            print(f"Assigned user changed to {new_user}")
        
        #User wants to edit the due date
        elif edit == 2:

            #Allows user to enter a date and edit the task
            due_date_edit = date_input()
            curr_task.due_date = due_date_edit

            #Updates task file
            write_task()
            print(f"Due date changed to {due_date_edit}")

    #If user wants to edit an already completed task
    else:
        print("You made a wrong choice, try again!")
        print("-----------------------------------")

    #If user has no tasks assigned
    if not has_task:
        print("You have no tasks.")
        print("-----------------------------------")

def percentage(number,total):
    """
    Function to return the percentage of two numbers
    number: int/float -> The subset of the set
    total: int/float -> The set
    """
    return round((number/total)*100,2)

def writeReports(task_file,user_file,task_string,user_string):
    """
    Writes report contents into text files

    task_file: string -> Name of task report file
    user_file: string -> Name of user report file
    task_string: list(string) -> lines to be written into task report file
    user_string: list(string) -> lines to be written into user report file
    """
    #Opens task and user overview files to be written in to
    with open(task_file,"w") as taskOverview, open(user_file,"w") as userOverview:
        
        #Loops through the list of task lines and writes them into the file
        for line in task_string:
            taskOverview.write(line)

        #Loops through the list of user lines and writes them into the file
        for line in user_string:
            userOverview.write(line)

def getReportInfo(users,userLen,tasks,taskLen):
    """
    Function to parse through all user and task info and generate a report
    Write report into the text file

    users: dict -> Of users and thier passwords
    userLen: int -> Number of users in system
    tasks: list -> Of task objects
    taskLen: int ->Number of tasks in system
    """

    #Gets todays date and converts it into a string
    today_date = datetime.today().strftime(DATETIME_STRING_FORMAT)

    #Header of user overview report 
    userStrings = [
        f"{'USER OVERVIEW REPORT':=<40}\n",
        f"Total tasks:   {taskLen}\n",
        f"Total users:   {userLen}\n\n"
        ]
    
    #Counters
    total_completed = 0 #Total number of completed tasks
    total_overdue   = 0   #Total number of overdue tasks
    
    #Loops through all users in system
    for user in users:

        #Counters
        user_tasks      = 0      #Number of tasks specific user has assigned
        user_completed  = 0  #Number of tasks specific user has completed
        user_overdue    = 0    #Number of tasks specific user has overdue
        
        #Loops through all tasks in system
        for task in tasks:
            #Increase counter if a task belongs to specific user
            if task.username == user:
                user_tasks += 1
                #Increase counter if task is completed
                if task.completed:
                    user_completed += 1
                #Incrase counter if NOT completed AND overdue
                elif str(task.due_date) < today_date:
                    user_overdue += 1

        #Increase total counters after the user has been parsed
        total_completed += user_completed
        total_overdue   += user_overdue

        #Calculates the number of incompleted tasks by user
        user_incomp = user_tasks-user_completed

        #Calculates percentages of user tasks 
        user_percent        = percentage(user_tasks,taskLen)
        user_comp_percent   = percentage(user_completed,user_tasks)
        user_incomp_percent = percentage(user_incomp,user_tasks)
        user_over_percent   = percentage(user_overdue,user_incomp)
        
        #List of lines containing user specific info
        #List is appended for each user.
        top_string = f"{user.title()}: INFORMATION"
        userStrings += [
                f"{top_string:=<40}\n",
                f"Tasks_____________{user_tasks}/{num_tasks:<5} ({user_percent}%)\n",
                f"Completed_________{user_completed}/{user_tasks:<5} ({user_comp_percent}%)\n",
                f"Incompleted_______{user_incomp}/{user_tasks:<5} ({user_incomp_percent}%)\n",
                f"Overdue___________{user_overdue}/{user_incomp:<5} ({user_over_percent}%)\n\n"
            ]

    #Calculates the number of incompleted tasks in total
    total_incompleted = taskLen-total_completed

    #Gets percentages of totals
    total_incomp_percent    = percentage(total_incompleted,taskLen) 
    total_over_percent      = percentage(total_overdue,taskLen)

    #List of lines containing task info
    taskStrings = [
        f"{'TASK OVERVIEW REPORT'}==================\n",
        f"Total tasks-----------{taskLen}\n",
        f"Completed tasks-------{total_completed}/{taskLen}\n",
        f"Incompleted tasks-----{total_incompleted}/{taskLen:<4} ({total_incomp_percent}%)\n",
        f"Overdue tasks---------{total_overdue}/{total_incompleted:<5} ({total_over_percent}%)"
    ]
    
    #Writes both reports to both files
    writeReports('task_overview.txt','user_overview.txt',taskStrings,userStrings)


#########################
# Main Program
######################### 

#Read tasks and generate a list of tasks
task_list = readTasks("tasks.txt")

#Read users and passwords and generates a dict
username_passwords = readUsers("user.txt")

#Login until valid
curr_user = login(username_passwords)

#The number of users in the system
num_users = len(username_passwords.keys())

#The number of tasks in the system
num_tasks = len(task_list)

while True:
    # Get input from user
    print()
    if curr_user == 'admin':
        menu = input('''Select one of the following Options below:
    r - Registering a user
    a - Adding a task
    va - View all tasks
    vm - view my task
    gr - generate reports
    ds - display statistics
    e - Exit
    : ''').lower()
    else:
        menu = input('''Select one of the following Options below:
    r - Registering a user
    a - Adding a task
    va - View all tasks
    vm - view my task
    e - Exit
    : ''').lower()

    if menu == 'r': # Register new user (if admin)
        # Request input of a new username
        if curr_user != 'admin':
            print("Registering new users requires admin privileges")
            continue
        
        #If user registration invalid, go back to menu
        if not reg_user():
            continue

    elif menu == 'a': # Add a new task
        #If added task is invalid, go back to menu
        if not add_task():
            continue


    elif menu == 'va': # View all tasks
        view_all()

    elif menu == 'vm': # View my tasks
        view_mine()

    elif menu == 'gr':
        #Generates task and user report text files
        getReportInfo(username_passwords,num_users,task_list,num_tasks)

    elif menu == 'ds' and curr_user == 'admin': # If admin, display statistics

        # If no overview files, generates it
        if not os.path.exists('task_overview.txt') or not os.path.exists('user_overview.txt'):
            print("Report not found. Generating...")
            getReportInfo(username_passwords,num_users,task_list,num_tasks)       

        #Get user selection for type of report
        print("Which report would you like to see?")
        print("1: Task overview")
        print("2: User overview")
        selection = int(input("Selection: "))

        #User wants to see task report
        if selection == 1:
            #Open task overview file and print each line
            with open('task_overview.txt','r') as taskOverview:
                for line in taskOverview:
                    print(line)
        
        #User wants to see user report
        elif selection == 2:
            #Open user overview file and print each line
            with open('user_overview.txt','r') as userOverview:
                for line in userOverview:
                    print(line)

    elif menu == 'e': # Exit program
        print('Goodbye!!!')
        exit()

    else: # Default case
        print("You have made a wrong choice, Please Try again")