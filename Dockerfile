# Base image
FROM python:3.8-slim-buster

# Create working directory
WORKDIR /app

ENV FLASK_APP main.py
ENV FLASK_RUN_PORT=5050

# Install required dependencies
RUN apt-get update -y && \
    apt-get install -y libpq-dev python3-dev python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install Flask gdown pandas numpy scikit-learn openpyxl flask-cors

ENV FLASK_RUN_HOST 0.0.0.0

# Copy application code
COPY requirements.txt requirements.txt

COPY . .

# Install local dependencies
RUN pip install -r requirements.txt

# Expose the port
EXPOSE 5050

# Entry point
CMD [ "flask" , "run"]