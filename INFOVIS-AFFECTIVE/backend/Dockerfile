# Use the official Python 3.12 image
FROM python:3.12

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install GDAL and its dependencies
RUN apt-get update && \
    apt-get install -y gdal-bin libgdal-dev && \
    apt-get clean

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Set the GDAL_CONFIG environment variable
ENV GDAL_CONFIG=/usr/bin/gdal-config

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Specify the command to run on container start
CMD ["python", "app.py"]
