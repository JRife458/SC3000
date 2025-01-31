## Setup Virtual Environment

### name of the virtual env - use whatever makes sense to you

python -m venv venv

### On Linux/macOS

source venv/bin/activate

### On Windows

venv\Scripts\activate

## Install Dependencies

pip install -r requirements.txt

## Database Setup and Migration

python manage.py migrate

### Optional

python manage.py createsuperuser

## Running App

python manage.py runserver

App should now be running on http://127.0.0.1:8000/

## Remember to deactivate the venv

deactivate
