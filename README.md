# Library-Management-System

### This repository contains a REST API using Django web development framework. It contains API's such as sign-up new users, see catalog and loaned books, loan and return books and get fees of users.

# Getting Started

#### Open terminal and run the clone this project
```
git clone https://github.com/IsraelDr/library-management.git
```
#### Create and activate virtual environment using
```
python -m venv .venv

. .\.venv\bin\activate (might be . .\.venv\script\activate)
```
#### The following dependencies might be needed:
```
pip install django 

pip3 install djangorestframework
 
pip install serializers

pip install django-oauth-toolkit
```
#### Run Steps to start the server and DB:
```  
python manage.py makemigrations

python manage.py migrate

python manage.py runserver
```
#### In order to see the admin page run the following steps:
```
python manage.py createsuperuser
```
##### Go to http://localhost:8000/admin/ and log in with your super user

#### In order to run REST request we need to authenticate. Therefore we need to define the app(thirdparty) that is using the library-management system.

#### Go to http://localhost:8000/o/applications/ and define app name, set Authorization grant type as 'Resource owner password-based' and keep the client id and client secret save. They will be part of the authantication.

#### Now you can start using the API. Examples from Postman attached.

