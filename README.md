# officer-survey-backend

## Setup

The first thing is to clone the repository

git clone git@github.com:Sarohy/officer-survey-backend.git
cd officer-survey-backend

# Install Dependencies

pip install -r requirements.txt

# DB Setup

Please follow the link for database setup and get NAME, USER, PASSWORD, HOST and PORT of your DB from your environment file

https://www.digitalocean.com/community/tutorials/how-to-use-postgresql-with-your-django-application-on-ubuntu-14-04

# Enironment Variable Setup

Make .env file
Copy .env-sample file to .env: cp .env-sample .env

# Runserver

python manage.py runserver

# Commands
python manage.py mysuperuser

python manage.py samplesurvey

python manage.py demo


# Google Translation 

You can add google cred file to bash file or you can just export it for terminal session

To export on terminal session

export GOOGLE_APPLICATION_CREDENTIALS = < path to the file>


# Staging Application

Staging Url: api.dev.officersurvey.com/super-admin

Credentials:

admin@officersurvey.com

!2!admin!2!

# Production Application

Production Url: api.officersurvey.com/super-admin
# Officer-Survey-Backend
