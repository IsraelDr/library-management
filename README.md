Library-Management-System

This repository contains a REST API using Django we development framework. It contains API's such as sign-up new users, see catalog and loaned books, loan and return books and get fees of users.

Getting Started

Open terminal and run the clone this project

git clone https://github.com/IsraelDr/library-management.git

Create and activate virtual environment using

virtualenv -p python3 venv

cd venv

source bin/activate (might be script/activate)

The following dependencies might be needed:

pip install django 

pip3 install djangorestframework
 
pip install serializers

pip install django-oauth-toolkit

Run Steps to start the server and DB:
   
python manage.py makemigrations

python manage.py migrate

python manage.py runserver

In order to see the admin page run the following steps:

python manage.py createsuperuser
