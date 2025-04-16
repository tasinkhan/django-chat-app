# Use an official Python runtime as a parent image
FROM python:3.12

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies (optional, based on your needs)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Make sure the wait-for-it.sh script is executable
# RUN chmod +x /app/wait-for-it.sh

# Expose the port Django will run on
EXPOSE 8000

# Run the Django application, waiting for the database to be ready before running migrations and starting the server
CMD ["bash", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
