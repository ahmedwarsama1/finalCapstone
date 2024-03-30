This app was created to create and save tasks to a notepad along with user login information

The admin account is able to perform the following tasks:

Register a new user
Add a new task
View all tasks
View all tasks assigned to you ( account currently logged in )
Generate reports
Display statistics
Other user accounts can perform the following tasks:

Add a new task
View all tasks
View all tasks assigned to you ( account currently logged in )
Generate reports
(other users also have the option to register a user, but will be displayed an error that only the admin can register new users). Other user accounts also do now have the option to Display Statistics on screen.

App functions
Register a new user
Registering a new user as the admin account will ask to enter a username and password ( the password will need to be confirmed twice ). The login details will be saved to a file called "user.txt" afterwards.

Add a new task
Adding a new task will request a username to assign the task to, a task title and description, and a due date. The creation date will automatically be added and the task will automatically be marked as not completed. The due date will be checked with the current date and cannot be set to a date prior to the current date. If a username is entered that's not registered, the user will be given a warning that the user is not registered. If the user is later registered, the task will be assigned to them by default.

View all tasks
This option allows you to view all tasks regardless of the user they are assigned to on screen.

View my tasks ( all tasks assigned to you )
This displays all tasks currently assigned to the user that's logged in. This allows you to also mark a task as "completed" . Once a task is marked as compelted it can no longer be edited. While a task is not completed it can be edited. Choosing to edit a task will loop you through the task creation process and allow you to assign a different or same user, assign a new title and description, and set a new due date. The new due date must also be the pressent day or later. If a username is entered that's not registered, the user will be given a warning that the user is not registered. If the user is later registered, the task will be assigned to them by default.

Generate reports
Choosing to Generate a report will create two text files:

task_overview.txt
user_overview.txt
user overview will display: Number of users registered in total Number of tasks created in total Number of tasks assigned to the user are Percentage of the total created tasks assigned to the user is Percentage of assigned tasks the user completed are Percentage of assigned tasks to the user that are uncompleted are Percentage of assigned tasks to the user that are overdue are

task overview will display: Number of tasks created in total Number of tasks completed Number of tasks uncompleted Number of tasks overdue Percentage of tasks uncompleted Percentage of tasks overdue

Display statistics (Only available to admin account)
This will display the statistics that have been saved to the text files with the "Generate report" function/ If no reports have been generated this will instead return an error
