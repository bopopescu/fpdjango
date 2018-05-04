# fpdjango

Before you start, Install MySQL, MySQL Server, and for optional reasons to see data tables download MySQL Workbench (optional)

In MySQL, create a user called 'django' with permissions to database 'freshpoint'

Make sure the database you make (called 'freshpoint') in MySQL matches these credentials below to connect the newly created
database to the application.

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'freshpoints',
        'USER': 'django',
        'PASSWORD': 'aggieprid3',
        'HOST': 'localhost',
        'PORT': '3306',
    }



Once you've successfully completed the steps above, next step is to ensure connection between the DB and the app

Make sure SQL Server is installed and running.

From the terminal:
in the project file location '.....fpdjango\freshpoint\freshpoint' you want to run the commands below:

type 'python manage.py makemigrations'
then type 'python manage.py migrate'

after you've done the steps above, you can now run the application
type this to run 'python manage.py runserver'
