# Use the official Python image from Docker Hub
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    build-essential \
    libssl-dev \
    libffi-dev \
    libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy your app files
COPY . /app

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install flask flask-cors flask-jwt-extended flask-mail mysql-connector-python werkzeug

# Expose the port your app runs on
EXPOSE 5000

# Run the application
CMD ["python", "yourfilename.py"]
