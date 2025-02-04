# Use an official Python runtime as a parent image
FROM python:3.13-alpine

# Set environment variables to improve performance and logging:
# - PYTHONDONTWRITEBYTECODE prevents Python from writing .pyc files.
# - PYTHONUNBUFFERED ensures output is sent immediately to logs.
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
# ENV PYTHONPATH=/app
ENV PYTHONPATH=/app/SC3000

# Set the working directory in the container to /app.
WORKDIR /app

# ENV GOOGLE_APPLICATION_CREDENTIALS=/app/SC3000/google_api.json

# Copy the requirements file into the container
COPY requirements.txt /app/

RUN pip install -r requirements.txt --progress-bar off

# Copy the entire project into the container.
# This will include your SC3000 folder (which contains manage.py and your project).
COPY . /app/

RUN python SC3000/manage.py collectstatic --noinput

# Run database migrations.
# This command runs at build time, so the SQLite database will be pre-seeded.
RUN python SC3000/manage.py migrate
RUN python SC3000/manage.py init_data
# Expose port 8080. Cloud Run typically expects your app to listen on port 8080.
EXPOSE 8080

# Should use gunicorn, need to use gunicorn
CMD gunicorn SC3000.wsgi:application --bind 0.0.0.0:8080 --workers 1
# CMD gunicorn SC3000.wsgi:application --bind 0.0.0.0:8080 --worker-class=gthread --threads=1 --workers 1
