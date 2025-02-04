# Sportscaster3000
![image](https://rollingferret.github.io/assets/myfiles/mlbgooglehackathon.png)

**Sportscaster3000** is a Django web application that summarizes recent games of your favorite teams using Google's Gemini AI and Google Text-to-Speech. It delivers concise game summaries and audio commentary powered by state-of-the-art AI technologies and is enriched with real-time statistics from MLB's Stats API.

## Features

- **AI Game Summaries:**  
  Automatically generates concise summaries of recent games for your favorite teams using Google Gemini AI.

- **Text-to-Speech Integration:**  
  Converts game summaries into speech using Google Text-to-Speech, allowing you to listen to the highlights.

- **MLB Stats Integration:**  
  Incorporates real-time data from MLB's Stats API to ensure game summaries are accurate and up-to-date.

- **User Profiles:**  
  Manage your user profile and select your favorite teams to receive personalized game updates.

- **Responsive Design:**  
  Built with Django and styled with Bootstrap for a clean, responsive user interface.

## Prerequisites

- Python 3.13 or newer
- pip (Python package installer)
- Virtual environment (recommended)

## Installation

### 1. Clone the Repository

git clone git@github.com:JRife458/SC3000.git

## 2. Setup Virtual Environment

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

## Create .env following .envtemplate. Will need to provide your own Google credentials.

### Optional

python manage.py createsuperuser

## Running App

python manage.py runserver

App should now be running on http://127.0.0.1:8000/

## Remember to deactivate the venv

deactivate
