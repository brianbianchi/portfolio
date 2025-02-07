# Use an official Python runtime as a parent image
FROM python:3.12-alpine

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /code

# Copy the current directory contents into the container at /code
COPY . /code/

# Install dependancies for Django project
RUN pip install --no-cache-dir -r requirements.txt

# Copy the cron job file into the container
COPY crontab /etc/crontabs/root

# Expose the port the app runs on
EXPOSE 8000

# Start cronjob and Django server
CMD crond -b & python manage.py runserver 0.0.0.0:8000