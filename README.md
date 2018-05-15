# fpdjango

Windows Installation Instructions

Prerequisite: 

1. Install MySQL Client/Server (or ensure access to a remote database) and Python Connector.
    Windows MySql instructions: https://dev.mysql.com/doc/refman/8.0/en/windows-installation.html
    
    Ensure the correct MySQL Python connector is installed. You can go to https://dev.mysql.com/downloads/connector/python/     and download the correct version for your system.
    
    Note: DJango is officially supported with PostgreSQL, MySQL, Oracle and SQLite. Any of these databases can be used as a       backend. Only Mysql has been tested with this application.

2. In MySQL, create a user called 'django' with permissions to database 'YourDB' (Name of your chosing)

3. Make sure the database you make in MySQL matches the credentials you set or will set in settings.py to connect the newly created database to the application.

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'YourDB',
        'USER': 'django',
        'PASSWORD': 'YourPassword',
        'HOST': 'YourHost',
        'PORT': 'YourPort',
    }

Instruction:

1. Make sure you have Python >= 2.7.9 installed
   Confirm what version of Python you are running this can be achieved by opening a command prompt and entering the            following:    python --version

2. Install virtual environment
    pip install virtualenv
    
3. Set up a virtual enironment for Django 
    cd c:\where\you\want\to\store\it
        virtualenv awesomeappenv

4. Activate virtual environemt:
    Do so by entering the following for Windows:
    \path\to\your\virtualenv\Scripts\activate
    We can confirm it is active by seeing (virtualenvname) before the CMD prompt
    
5. Install Django with MySql Database Capabilities
    pip install django mysqlclient

6. Clone this repository: git clone https://github.com/DSwift510/fpdjango.git

    type 'pip install -r \path\to\requirements.txt'
    
Once you've successfully completed the steps above, the next step is to ensure connection between the DB and the app

Make sure SQL Server is installed and running.

From the terminal:
in the project file location 'path\to\fpdjango\freshpoint\freshpoint' you want to run the commands below:

type 'python manage.py makemigrations'
then type 'python manage.py migrate'
finally you can now run the application
type this to run 'python manage.py runserver'

--------------------
Helpful Links

How to Install Django: https://docs.djangoproject.com/en/2.0/topics/install/

How do I run this Django Python Github Project on Windows: https://www.quora.com/How-do-I-run-this-Django-Python-Github-Project-on-Windows
