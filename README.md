# POC-CRQ-Intelligence
This repository is for the POC development of the Patch CRQ Intelligence platform.
This is a django based application


# CRQ_Intelligence - Project Creation
django-admin startproject crq_project
cd .\crq_project\
python manage.py startapp crq_app

# Start LocalHost
python manage.py migrate
python manage.py runserver

# Add the required .env file to the below path
crq_project/crq_app/.env

# Create SuperUser
python manage.py createsuperuser --username=admin --email=admin@sce.com