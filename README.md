# fsf_2019_screening_task1
A very simple Task Management web app written with Django

## Features

1. Authenticate the user<br>
    - Allows new users to sign up<br>
    - Allows existing users to sign in<br>
2. Allows only an authenticated user to create Task<br>
3. Allows creation of ‘Teams’<br>
    - Team creator should be able to add other Users to their Teams<br>
4. Only the Task Creator can edit Tasks that have been created by himself<br>
    - Other users from the same team can only view and comment on Tasks that were created by another User<br>
    - A User from another Team cannot view/edit/assign/comment on a Task of a different Team Member.<br>
    - Creator of Task should be able to assign the Task to one or more Users from his own Team<br>
5. Tasks have the Fields: Title, Description, Assignee, and Status (Planned, Inprogress, Done etc.)<br>
    - Each Task is having a comments section where all users in one Team can comment on the Task<br>
    - An authenticated User can comment on his own tasks (assigned to or created by him) as well as other Tasks of his Team members.<br>

# Requirements
- Python 3.5+ (tested with Python 3.6).
- Django 2.1 and other dependencies declared in the requirements.txt file.
- A Django compatible database PostgreSQL (by default uses the Python's built-in SQLite database ).

# Install and Run
(Optional) Create a virtual environment and activate it with:
<pre>$ python3 -m venv .venv && source .venv/bin/activate</pre>
Install dependencies with:
<pre>$ pip install -r requirements.txt</pre>
Create the database with:
 - CREATE DATABASE database_name(in psql command line)
 - Change the NAME of the database in settings.py file
 - Change the USER according to your POSTGRES USER in settings.py file
 - Change the PASSWORD in settings.py file
 
Migrating Database:
<pre>$ python3 manage.py makemigrations
$ python3 manage.py migrate</pre>
To create an admin user:
<pre>$ python3 manage.py createsuperuser</pre>
Then run in development mode with:
<pre>$ python3 manage.py runserver</pre>
# Access the application
Like any Django app developed with Django, enter with: http://localhost:8000
# Test&Coverage
- Ran 30 tests in 5.244s
- Coverage of **98%**
- For more detail analysis on coverage check **htmlcov/index.html**

# Screenshorts
![Login](TaskManager/static/login.png)
![SignUp](TaskManager/static/Signup.png)
![Home](TaskManager/static/Home Page.png)
![User Detail](TaskManager/static/user.png)
![Team Detail](TaskManager/static/Team.png)
![Task Detail](TaskManager/static/Task.png)
![Edit Task](TaskManager/static/Edit_Task.png)
![Comment](TaskManager/static/Comment.png)
