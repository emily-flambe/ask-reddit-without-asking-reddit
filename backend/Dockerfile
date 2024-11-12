# Dockerfile

# Use an official Python image as the base
FROM python:3.12-slim

# Define build arguments to pass environment variables from docker-compose.yml
ARG FLASK_APP
ARG FLASK_ENV
ARG CLIENT_ID
ARG CLIENT_SECRET
ARG REFRESH_TOKEN
ARG DATABASE_URL

# Set environment variables for runtime
ENV FLASK_APP=$FLASK_APP
ENV FLASK_ENV=$FLASK_ENV
ENV CLIENT_ID=$CLIENT_ID
ENV CLIENT_SECRET=$CLIENT_SECRET
ENV REFRESH_TOKEN=$REFRESH_TOKEN
ENV DATABASE_URL=$DATABASE_URL

# Create a working directory in the container
WORKDIR /app

# Copy requirements.txt first to leverage Docker's cache if requirements haven't changed
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /app

# Expose the port the Flask app will run on
EXPOSE 5000

# Run the Flask application
CMD ["flask", "run", "--host=0.0.0.0"]
